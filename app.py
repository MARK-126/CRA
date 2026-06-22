import streamlit as st
from streamlit_folium import st_folium

from src.data_loader import load_departments, load_health_centers, POPULATION_DATA
from src.map_builder import build_map
from src.charts import (
    build_centers_by_dept_chart,
    build_sector_donut_chart,
    build_financing_breakdown_chart,
    build_centers_per_capita_chart,
)

st.set_page_config(
    page_title="Salud Mendoza",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0c0c0e; }

    section[data-testid="stSidebar"] {
        background-color: #111114 !important;
        border-right: 1px solid #222228 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f4f4f5 !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #a1a1aa !important;
    }

    h1, h2, h3 { color: #f4f4f5 !important; font-weight: 700 !important; }
    p { color: #a1a1aa; }

    div[data-testid="metric-container"] {
        background-color: rgba(24, 24, 27, 0.45);
        border-radius: 12px;
        padding: 1.25rem 1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .stApp div[data-testid="stMetricValue"],
    .stApp div[data-testid="stMetricValue"] * {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #f97316 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #a1a1aa !important;
        font-weight: 500 !important;
    }

    .stTabs [data-baseweb="tab"] { color: #71717a !important; }
    .stTabs [aria-selected="true"] {
        color: #f4f4f5 !important;
        border-bottom-color: #6366f1 !important;
    }

    .stAlert {
        background-color: #18181b !important;
        color: #f4f4f5 !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
    }

    hr { border-color: #27272a !important; margin: 1.5rem 0 !important; }

    header[data-testid="stHeader"] {
        background-color: #0c0c0e !important;
        border-bottom: 1px solid #222228 !important;
    }

    .block-container {
        max-width: 1200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
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
    ["Inicio", "Mapa e Interactividad", "Estadísticas y Conclusiones"],
)



if page == "Inicio":
    total_pop = sum(POPULATION_DATA.values())
    n_depts = df_centers["departamento_nombre"].nunique()

    col_left, col_right = st.columns([1.2, 1], gap="medium")

    with col_left:
        st.markdown("""
        <div style="padding: 3rem 1.5rem 3rem 0; display: flex; flex-direction: column; justify-content: center; min-height: 480px;">
            <div style="
                display: inline-block;
                background: rgba(99, 102, 241, 0.05);
                border: 1px solid rgba(99, 102, 241, 0.25);
                border-radius: 6px;
                padding: 4px 14px;
                margin-bottom: 2rem;
                width: fit-content;
            ">
                <span style="color: #818cf8; font-size: 0.72rem; letter-spacing: 0.12em;
                             text-transform: uppercase; font-weight: 700;">
                    Proyecto Integrador · CRA 2025
                </span>
            </div>
            <div style="
                font-size: 4.5rem;
                font-weight: 850;
                background: linear-gradient(135deg, #a5b4fc 0%, #6366f1 50%, #38bdf8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.08;
                letter-spacing: -0.03em;
                margin: 0 0 1.75rem 0;
            ">
                Análisis<br>Territorial de<br>Centros de Salud<br>en Mendoza
            </div>
            <p style="font-size: 1rem; color: #a1a1aa; line-height: 1.8; margin: 0; max-width: 400px;">
                Exploración geoespacial y estadística de los efectores del sistema de salud,
                su distribución territorial y accesibilidad poblacional.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='padding-top: 3rem;'>", unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Establecimientos", f"{len(df_centers):,}".replace(",", "."))
        with m2:
            st.metric("Habitantes", f"{total_pop:,}".replace(",", "."))
        with m3:
            st.metric("Departamentos", n_depts)

        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(24, 24, 27, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px;
                    padding: 1.5rem 1.75rem; margin-bottom: 0.75rem;">
            <p style="color: #818cf8; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em;
                      text-transform: uppercase; margin: 0 0 0.9rem 0;">
                Objetivos del análisis
            </p>
            <ul style="color: #d4d4d8; line-height: 2; margin: 0; padding-left: 1.1rem; font-size: 0.88rem;">
                <li>Identificar zonas sin cobertura sanitaria adecuada</li>
                <li>Analizar el balance público–privado de efectores</li>
                <li>Calcular la tasa de centros de salud por habitante</li>
                <li>Generar propuestas de política pública basadas en datos</li>
            </ul>
        </div>
        <div style="background: rgba(24, 24, 27, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px;
                    padding: 1.5rem 1.75rem;">
            <p style="color: #818cf8; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em;
                      text-transform: uppercase; margin: 0 0 0.9rem 0;">
                Fuentes de datos
            </p>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <span style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); color: #a1a1aa; padding: 4px 12px;
                             border-radius: 20px; font-size: 0.8rem; font-weight: 500;">REFES</span>
                <span style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); color: #a1a1aa; padding: 4px 12px;
                             border-radius: 20px; font-size: 0.8rem; font-weight: 500;">GeoRef</span>
                <span style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); color: #a1a1aa; padding: 4px 12px;
                             border-radius: 20px; font-size: 0.8rem; font-weight: 500;">INDEC · Censo 2022</span>
                <span style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); color: #a1a1aa; padding: 4px 12px;
                             border-radius: 20px; font-size: 0.8rem; font-weight: 500;">Datos Abiertos Argentina</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


elif page == "Mapa e Interactividad":
    st.title("Mapa de Cobertura y Efectores de Salud")

    st.sidebar.subheader("Filtros del Mapa")

    depts = sorted(df_centers["departamento_nombre"].unique())
    selected_depts = st.sidebar.multiselect("Filtrar por Departamento(s):", depts, default=[])

    sectors = sorted(df_centers["origen_financiamiento"].unique())
    selected_sectors = st.sidebar.multiselect("Filtrar por Sector:", sectors, default=sectors)

    tipologies = sorted(df_centers["tipologia_nombre"].unique())
    selected_tipologies = st.sidebar.multiselect(
        "Filtrar por Tipo de Establecimiento:", tipologies, default=[]
    )

    buffer_radius = st.sidebar.slider(
        "Área de influencia / Cobertura (km):", 0.0, 10.0, 0.0, step=0.5
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

    st.markdown(
        f"Mostrando **{len(df_filtered)}** establecimientos según los filtros seleccionados."
    )

    map_placeholder = st.empty()
    map_placeholder.markdown("""
    <div style="
        height: 550px;
        background: #111114;
        border-radius: 12px;
        border: 1px solid #27272a;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1.25rem;
    ">
        <div style="
            width: 48px; height: 48px;
            border: 3px solid #27272a;
            border-top-color: #6366f1;
            border-radius: 50%;
            animation: map-spin 0.75s linear infinite;
        "></div>
        <p style="color: #52525b; font-size: 0.875rem; margin: 0; letter-spacing: 0.03em;">
            Cargando mapa...
        </p>
    </div>
    <style>
        @keyframes map-spin { to { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)

    m = build_map(df_filtered, gdf_deps_filtered, buffer_radius)
    map_placeholder.empty()

    st.markdown("""
    <style>
    .folium-wrap { position: relative; }
    .folium-overlay {
        position: absolute; inset: 0;
        background: #111114;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center; gap: 1.25rem;
        z-index: 9999; border-radius: 8px;
        transition: opacity 0.4s ease;
    }
    @keyframes folium-spin { to { transform: rotate(360deg); } }
    </style>
    <script>
    (function () {
        const POLL_MS = 100;
        const MAX_WAIT = 15000;
        let elapsed = 0;

        function attachOverlay(iframe) {
            const wrap = iframe.closest('[data-testid="stIframe"]') || iframe.parentElement;
            if (!wrap || wrap.dataset.overlayAttached) return;
            wrap.dataset.overlayAttached = "1";
            wrap.style.position = "relative";

            const overlay = document.createElement("div");
            overlay.className = "folium-overlay";
            overlay.innerHTML = `
                <div style="width:48px;height:48px;border:3px solid #27272a;
                            border-top-color:#6366f1;border-radius:50%;
                            animation:folium-spin 0.75s linear infinite;"></div>
                <p style="color:#52525b;font-size:0.875rem;margin:0;letter-spacing:0.03em;">
                    Cargando mapa...
                </p>`;
            wrap.appendChild(overlay);

            iframe.addEventListener("load", () => {
                overlay.style.opacity = "0";
                setTimeout(() => overlay.remove(), 400);
            }, { once: true });
        }

        function poll() {
            const iframe = document.querySelector('iframe[title="streamlit_folium.st_folium"]')
                        || document.querySelector('.stIframe iframe');
            if (iframe) {
                attachOverlay(iframe);
                return;
            }
            elapsed += POLL_MS;
            if (elapsed < MAX_WAIT) setTimeout(poll, POLL_MS);
        }

        poll();
    })();
    </script>
    """, unsafe_allow_html=True)

    st_folium(m, width="100%", height=550, returned_objects=[])

    st.subheader("Listado de Establecimientos")
    st.dataframe(
        df_filtered[[
            "establecimiento_nombre",
            "departamento_nombre",
            "origen_financiamiento",
            "tipologia_nombre",
            "domicilio",
        ]].rename(columns={
            "establecimiento_nombre": "Nombre",
            "departamento_nombre": "Departamento",
            "origen_financiamiento": "Sector",
            "tipologia_nombre": "Tipo",
            "domicilio": "Dirección",
        }),
        use_container_width=True,
    )


elif page == "Estadísticas y Conclusiones":
    st.title("Análisis Estadístico y Diagnóstico")

    tab1, tab2 = st.tabs(["Gráficos de Distribución", "Diagnóstico y Conclusiones"])

    with tab1:
        st.subheader("Métricas de Capacidad e Infraestructura")

        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown("##### Cantidad de Centros de Salud por Departamento")
            fig1 = build_centers_by_dept_chart(df_centers)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown("##### Gestión Pública vs. Privada")
            fig2 = build_sector_donut_chart(df_centers)
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        col3, col4 = st.columns([2, 3], gap="large")

        with col3:
            st.markdown("##### Desglose por Origen de Financiamiento")
            fig3 = build_financing_breakdown_chart(df_centers)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown("##### Centros de Salud por cada 10.000 Habitantes (Censo 2022)")
            fig4 = build_centers_per_capita_chart(df_centers, POPULATION_DATA)
            st.plotly_chart(fig4, use_container_width=True)

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
