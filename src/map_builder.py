import folium
import geopandas as gpd
from folium.plugins import MarkerCluster

def build_map(df_centers, gdf_deps, buffer_radius_km=0.0):
    """
    Genera un mapa interactivo de Folium con centros de salud y polígonos departamentales.
    
    Args:
        df_centers (pd.DataFrame): DataFrame con datos de centros de salud.
        gdf_deps (gpd.GeoDataFrame): GeoDataFrame con polígonos departamentales.
        buffer_radius_km (float): Radio en kilómetros para buffers alrededor de centros (0.0 para desactivar).
    
    Returns:
        folium.Map: Objeto de mapa Folium renderizado.
    """
    
    m = folium.Map(location=[-34.0, -68.5], zoom_start=7, tiles="cartodbpositron")
    
    style_function = lambda x: {
        "fillColor": "#115e59",
        "color": "#0f766e",
        "weight": 1.5,
        "fillOpacity": 0.15
    }
    
    folium.GeoJson(
        gdf_deps,
        style_function=style_function,
        highlight_function=lambda x: {"fillOpacity": 0.35, "weight": 2.5},
        tooltip=folium.GeoJsonTooltip(fields=["nombre"], aliases=["Departamento:"])
    ).add_to(m)
    
    marker_cluster = MarkerCluster(
        options={
            "showCoverageOnHover": False,
            "spiderfyOnMaxZoom": True
        }
    ).add_to(m)
    
    for _, row in df_centers.iterrows():
        lat = row["latitud"]
        lon = row["longitud"]
        name = row["establecimiento_nombre"]
        address = row["domicilio"]
        sector = row["origen_financiamiento"]
        tipology = row["tipologia_nombre"]
        
        popup_html = f"""
        <div style="font-family: sans-serif; color: #042f2e; font-size: 12px; line-height: 1.4; padding: 5px;">
            <b style="color: #0f766e; font-size: 13px;">{name}</b><br><br>
            <b>Tipo:</b> {tipology}<br>
            <b>Sector:</b> {sector}<br>
            <b>Dirección:</b> {address}
        </div>
        """
        
        color = "#0f766e" if str(sector).lower() == "público" else "#0d9488"
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=250)
        ).add_to(marker_cluster)
        
        if buffer_radius_km > 0.0:
            folium.Circle(
                location=[lat, lon],
                radius=float(buffer_radius_km) * 1000,
                color="#0f766e",
                weight=1,
                fill=True,
                fill_color="#0f766e",
                fill_opacity=0.05
            ).add_to(m)
            
    return m
