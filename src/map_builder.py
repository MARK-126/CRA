import folium
from folium.plugins import MarkerCluster


def build_map(df_centers, gdf_deps, buffer_radius_km=0.0):
    m = folium.Map(location=[-34.0, -68.5], zoom_start=7, tiles="cartodbdark_matter")

    if not gdf_deps.empty:
        folium.GeoJson(
            gdf_deps,
            style_function=lambda x: {
                "fillColor": "#6366f1",
                "color": "#818cf8",
                "weight": 1.5,
                "fillOpacity": 0.08,
            },
            highlight_function=lambda x: {"fillOpacity": 0.25, "weight": 2.5},
            tooltip=folium.GeoJsonTooltip(fields=["nombre"], aliases=["Departamento:"]),
        ).add_to(m)

    marker_cluster = MarkerCluster(
        options={"showCoverageOnHover": False, "spiderfyOnMaxZoom": True}
    ).add_to(m)

    for _, row in df_centers.iterrows():
        lat = row["latitud"]
        lon = row["longitud"]
        name = row["establecimiento_nombre"]
        sector = row["origen_financiamiento"]

        popup_html = f"""
        <div style="font-family: sans-serif; font-size: 12px; line-height: 1.6; padding: 6px; min-width: 200px;">
            <b style="color: #6366f1; font-size: 13px;">{name}</b><br><br>
            <b>Tipo:</b> {row['tipologia_nombre']}<br>
            <b>Sector:</b> {sector}<br>
            <b>Dirección:</b> {row['domicilio']}
        </div>
        """

        color = "#6366f1" if str(sector).lower() == "público" else "#f59e0b"

        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=260),
        ).add_to(marker_cluster)

        if buffer_radius_km > 0.0:
            folium.Circle(
                location=[lat, lon],
                radius=float(buffer_radius_km) * 1000,
                color="#6366f1",
                weight=1,
                fill=True,
                fill_color="#6366f1",
                fill_opacity=0.05,
            ).add_to(m)

    return m
