# Justificación de Tecnologías Utilizadas

## Contexto del proyecto

Aplicación web de análisis geoespacial y estadístico de centros de salud en Mendoza, con datos provenientes de REFES, GeoRef Argentina e INDEC (Censo 2022).

---

## Stack principal

### Python
Lenguaje central del proyecto. Ecosistema maduro para análisis de datos, amplia disponibilidad de librerías geoespaciales y estadísticas, y bajo costo de entrada para proyectos académicos.

### Streamlit
Framework para construir la interfaz web interactiva. Permite convertir scripts Python en dashboards sin necesidad de desarrollar frontend por separado (HTML/JS/CSS), reduciendo la complejidad del proyecto a una sola capa de código. Su sistema de caché (`@st.cache_data`) evita recargar datos en cada interacción del usuario.

### Pandas
Manipulación y filtrado del dataset de establecimientos (REFES). Ofrece lectura directa de CSV remotos, selección de columnas, filtrado por provincia y limpieza de coordenadas inválidas con una API concisa y bien documentada.

### GeoPandas
Extensión geoespacial de Pandas. Permite leer el GeoJSON de departamentos desde la API GeoRef, operar con geometrías (polígonos, buffers de cobertura) y reproyectar coordenadas (EPSG:4326) sin abandonar el paradigma de DataFrames. Es la alternativa estándar en Python para SIG vectorial sin necesidad de un servidor de bases de datos espaciales.

### Shapely
Usada internamente por GeoPandas para las operaciones de geometría (cálculo de buffers de área de influencia en el mapa). No requiere configuración adicional; viene como dependencia del stack geoespacial Python.

### Folium + streamlit-folium
Folium genera mapas interactivos basados en Leaflet.js. `streamlit-folium` lo integra dentro de Streamlit como componente embebido. Alternativa elegida frente a Kepler.gl o Deck.gl por su facilidad de uso en Python y por no requerir tokens de API externos para tiles base.

### Plotly
Librería de visualización para los gráficos estadísticos (barras, donut, scatter). Produce gráficos interactivos (hover, zoom) que se integran nativamente con `st.plotly_chart`. Se eligió sobre Matplotlib/Seaborn por ser interactivo por defecto y mantener coherencia visual con el tema oscuro del dashboard.

### Requests
Descarga de datos desde fuentes externas (API GeoRef, REFES). Librería HTTP estándar de Python; usada para la primera carga con cache local en disco, eliminando dependencias de red en ejecuciones posteriores.

### openpyxl
Dependencia para que Pandas pueda leer/escribir archivos `.xlsx` en caso de que los datos fuente se distribuyan en ese formato. Incluida de forma preventiva por compatibilidad con fuentes oficiales argentinas que suelen publicar datos en Excel.

---

## Decisiones de arquitectura

| Necesidad | Herramienta elegida | Alternativa descartada | Motivo |
|---|---|---|---|
| Interfaz web | Streamlit | Flask + React | Menor costo de desarrollo; proyecto académico |
| Mapas interactivos | Folium | Deck.gl / Kepler.gl | Sin API key; integración directa con Python |
| Gráficos | Plotly | Matplotlib | Interactividad nativa; compatibilidad tema oscuro |
| Datos geoespaciales | GeoPandas | PostGIS | Sin servidor; suficiente para escala provincial |
| Fuente geográfica | GeoRef Argentina | OSM / Google Maps | API pública, oficial y gratuita del Estado Nacional |
