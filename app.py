import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium

from src.data_loader import load_departments, load_health_centers, POPULATION_DATA
from src.map_builder import build_map
from src.charts import build_centers_by_dept_chart, build_sector_distribution_chart, build_centers_per_capita_chart

st.set_page_config(
    page_title="Salud Mendoza",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    div[data-testid="metric-container"] {
        background-color: #115e59;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #0f766e;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 600;
        color: #ccfbf1;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #99f6e4;
        font-weight: 500;
        margin-bottom: 8px;
    }
    h1, h2, h3 {
        color: #ccfbf1 !important;
        font-weight: 600 !important;
    }
    .stAlert {
        background-color: #115e59 !important;
        color: #ccfbf1 !important;
        border: 1px solid #0f766e !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_cached_data():
    gdf_deps = load_departments()
    df_centers = load_health_centers()
    return gdf_deps, df_centers

try:
    gdf_deps, df_centers = get_cached_data()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

st.sidebar.title("Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["Inicio y Contexto", "Mapa e Interactividad", "Estadísticas y Conclusiones"]
)

if page == "Inicio y Contexto":
    st.title("Estudio de Centros de Salud en la Provincia de Mendoza")
    
    st.markdown("""
    Este proyecto integrador analiza la **distribución territorial y accesibilidad** de los establecimientos de salud en la provincia de Mendoza. 
    A través de este diagnóstico, se busca identificar disparidades geográficas y proponer mejoras en la cobertura de salud pública.
    
    Utilizando datos del **Registro Federal de Establecimientos de Salud (REFES)** y límites departamentales de la **Dirección Nacional de Datos Abiertos (Georef)**, 
    cruzamos la ubicación de los efectores de salud con los datos de población definitivos del **Censo 2022**.
    """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total de Establecimientos Georreferenciados",
            value=len(df_centers)
        )
    with col2:
        total_pop = sum(POPULATION_DATA.values())
        st.metric(
            label="Población Total (Censo 2022)",
            value=f"{total_pop:,}".replace(",", ".")
        )
    with col3:
        public_centers = len(df_centers[df_centers["origen_financiamiento"].str.lower() == "público"])
        st.metric(
            label="Establecimientos de Gestión Pública",
            value=public_centers
        )
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.subheader("Objetivos del Análisis")
    st.markdown("""
    *   **Identificar zonas desatendidas:** Detectar áreas residenciales alejadas de los centros de asistencia primaria.
    *   **Analizar la relación público-privado:** Comprender el balance de efectores según su origen de financiamiento.
    *   **Calcular el indicador de centros por habitante:** Comparar la disponibilidad de recursos sanitarios entre departamentos.
    *   **Generar propuestas basadas en datos:** Plantear políticas de infraestructura y asignación de recursos.
    """)

elif page == "Mapa e Interactividad":
    st.title("Mapa de Cobertura y Efectores de Salud")
    
    st.sidebar.subheader("Filtros del Mapa")
    
    depts = sorted(df_centers["departamento_nombre"].unique())
    selected_depts = st.sidebar.multiselect(
        "Filtrar por Departamento(s):",
        depts,
        default=[]
    )
    
    sectors = sorted(df_centers["origen_financiamiento"].unique())
    selected_sectors = st.sidebar.multiselect(
        "Filtrar por Sector:",
        sectors,
        default=sectors
    )
    
    tipologies = sorted(df_centers["tipologia_nombre"].unique())
    selected_tipologies = st.sidebar.multiselect(
        "Filtrar por Tipo de Establecimiento:",
        tipologies,
        default=[]
    )
    
    buffer_radius = st.sidebar.slider(
        "Área de influencia / Cobertura (km):",
        min_value=0.0,
        max_value=10.0,
        value=0.0,
        step=0.5
    )
    
    df_filtered = df_centers.copy()
    if selected_depts:
        df_filtered = df_filtered[df_filtered["departamento_nombre"].isin(selected_depts)]
    if selected_sectors:
        df_filtered = df_filtered[df_filtered["origen_financiamiento"].isin(selected_sectors)]
    if selected_tipologies:
        df_filtered = df_filtered[df_filtered["tipologia_nombre"].isin(selected_tipologies)]
        
    gdf_deps_filtered = gdf_deps.copy()
    if selected_depts:
        gdf_deps_filtered = gdf_deps_filtered[gdf_deps_filtered["nombre"].isin(selected_depts)]
        
    st.markdown(f"Mostrando **{len(df_filtered)}** establecimientos de salud según los filtros seleccionados.")
    
    m = build_map(df_filtered, gdf_deps_filtered, buffer_radius)
    st_folium(m, width="100%", height=550, returned_objects=[])
    
    st.subheader("Listado de Establecimientos")
    st.dataframe(
        df_filtered[[
            "establecimiento_nombre", 
            "departamento_nombre", 
            "origen_financiamiento", 
            "tipologia_nombre", 
            "domicilio"
        ]].rename(columns={
            "establecimiento_nombre": "Nombre",
            "departamento_nombre": "Departamento",
            "origen_financiamiento": "Sector",
            "tipologia_nombre": "Tipo",
            "domicilio": "Dirección"
        }),
        use_container_width=True
    )

elif page == "Estadísticas y Conclusiones":
    st.title("Análisis Estadístico y Diagnóstico")
    
    tab1, tab2 = st.tabs(["Gráficos de Distribución", "Diagnóstico y Conclusiones"])
    
    with tab1:
        st.subheader("Métricas de Capacidad e Infraestructura")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Cantidad de Centros de Salud por Departamento")
            fig1 = build_centers_by_dept_chart(df_centers)
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            st.markdown("##### Distribución según Origen de Financiamiento")
            fig2 = build_sector_distribution_chart(df_centers)
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("##### Centros de Salud por cada 10.000 Habitantes (Censo 2022)")
        fig3 = build_centers_per_capita_chart(df_centers, POPULATION_DATA)
        st.plotly_chart(fig3, use_container_width=True)
        
    with tab2:
        st.subheader("Diagnóstico de Cobertura Territorial")
        st.markdown("""
        A partir del análisis geográfico y estadístico de los efectores en Mendoza, se desprenden las siguientes observaciones clave:
        
        *   **Concentración en el Gran Mendoza:** Departamentos como Capital y Godoy Cruz concentran una mayor densidad absoluta de centros de salud y hospitales de alta complejidad. Sin embargo, su tasa de establecimientos por habitante se ve matizada por la alta densidad poblacional.
        *   **Desiertos de Cobertura Rural:** En departamentos extensos pero de menor densidad poblacional (como Malargüe, Lavalle y San Carlos), los centros de asistencia primaria se encuentran muy distanciados entre sí. Aumentar el buffer de cobertura a 5 km revela que amplios sectores rurales quedan fuera de un rango de atención razonable.
        *   **Predominancia de la Gestión Pública:** El sector público representa el sostén principal de la atención primaria, especialmente en las zonas alejadas de las cabeceras departamentales, mientras que las clínicas privadas se concentran fuertemente en las zonas comerciales del Gran Mendoza.
        """)
        
        st.subheader("Propuestas de Políticas Públicas")
        st.markdown("""
        1.  **Redistribución de Centros de Atención Primaria (CAPS):** Diseñar unidades móviles de salud que recorran de manera planificada los parajes rurales y periféricos de Lavalle, Malargüe y La Paz para paliar las grandes distancias.
        2.  **Optimización del Transporte Sanitario:** Reforzar la flota de ambulancias y el sistema de traslados programados en los departamentos periféricos para asegurar la conexión con los hospitales de cabecera.
        3.  **Fomento de la Telemedicina:** Implementar puntos de consulta digital en centros de salud rurales, permitiendo diagnósticos y seguimientos de especialistas desde el Gran Mendoza sin obligar al paciente a trasladarse.
        """)
