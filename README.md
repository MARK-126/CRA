# 🏥 Estudio de Centros de Salud en la Provincia de Mendoza
## Proyecto Integrador - materia: *Comunicación de Resultados Analíticos*

Este proyecto consiste en una aplicación web interactiva desarrollada con **Streamlit**, **GeoPandas** y **Folium** para el análisis geoespacial y estadístico de los efectores de salud en la provincia de Mendoza, Argentina. 

El desarrollo se enfoca en resolver el **Tema 2: "Centros de Salud de Mendoza"** según las directrices establecidas en el documento de consignas `parcial.pdf`.

---

## 📋 Alineación con las Consignas del Proyecto (`parcial.pdf`)

A continuación se detalla cómo el proyecto implementa cada uno de los requerimientos de la consigna:

1. **Buscar un dataset real y analizar datos:**
   - **Efectores de salud:** Se consumen datos del **Registro Federal de Establecimientos de Salud (REFES)** actualizados a nivel nacional, filtrando específicamente los correspondientes a la provincia de Mendoza.
   - **Límites geográficos:** Se utilizan los límites departamentales provistos por la **Dirección Nacional de Datos Abiertos (Georef API)**.
   - **Datos demográficos:** Se incorporan los datos definitivos de población del **Censo Nacional 2022** para cada uno de los 18 departamentos de Mendoza.

2. **Mostrar la ubicación de hospitales, centros de salud y su distribución territorial:**
   - La aplicación categoriza los establecimientos según su tipología (Hospitales, Centros de Salud, CAPS, etc.) e integra sus coordenadas exactas (latitud y longitud) en un mapa georreferenciado.

3. **Mapa Interactivo:**
   - Implementado en la sección **"Mapa e Interactividad"** usando **Folium**. Permite:
     - Filtrar dinámicamente por uno o más departamentos.
     - Filtrar por sector (Público vs. Privado/Otros).
     - Filtrar por tipología del establecimiento.
     - **Área de influencia (Buffer):** Deslizador dinámico que permite proyectar un radio de cobertura (de 0 a 10 km) alrededor de cada centro para evaluar la accesibilidad y los desiertos de cobertura.
     - Agrupamiento (*Marker Clustering*) para facilitar la navegación visual cuando hay alta densidad de efectores.

4. **Gráficos de cantidad y análisis por departamento:**
   - Implementado en la sección **"Estadísticas y Conclusiones"** usando **Plotly**:
     - *Cantidad absoluta:* Gráfico de barras horizontales con gradiente de color (indigo → naranja) según la cantidad de centros por departamento.
     - *Distribución por sector:* Gráfico de dona interactivo con el porcentaje de establecimientos públicos frente a los privados.
     - *Desglose por financiamiento:* Treemap que muestra la proporción de cada origen de financiamiento de forma jerárquica y visual.
     - *Tasa de cobertura per cápita:* Lollipop chart que calcula la cantidad de **Centros de Salud por cada 10.000 habitantes** cruzando los datos del Censo 2022, con puntos coloreados por valor.

5. **Conclusiones y Recomendaciones:**
   - La aplicación presenta un diagnóstico detallado sobre la concentración de recursos en el Gran Mendoza, los desiertos sanitarios en áreas rurales (Lavalle, Malargüe, San Carlos) y propone tres políticas públicas basadas en los resultados (Redistribución/CAPS móviles, Optimización de transporte sanitario y Telemedicina rural).

---

## 🛠️ Estructura del Código

La arquitectura del proyecto está organizada de manera modular para garantizar la escalabilidad y limpieza del código:

```text
CRA/
│
├── .streamlit/
│   └── config.toml         # Configuración visual y del tema oscuro de Streamlit.
│
├── data/                   # Carpeta para almacenamiento local de los datasets cacheables.
│   ├── mendoza_departments.geojson
│   └── mendoza_health_centers.csv
│
├── src/                    # Módulos con la lógica de negocio.
│   ├── charts.py           # Construcción de gráficos Plotly.
│   ├── data_loader.py      # Conexión con APIs, descargas de CSV/GeoJSON, y datos del Censo.
│   └── map_builder.py      # Lógica de renderizado del mapa de Folium.
│
├── app.py                  # Punto de entrada principal de Streamlit (interfaz y navegación).
├── Dockerfile              # Configuración de Docker para contenerización.
├── docker-compose.yml      # Configuración de Docker Compose para despliegue simplificado.
├── parcial.pdf             # Archivo original con las directrices del proyecto.
└── requirements.txt        # Dependencias de Python necesarias.
```

---

## 🚀 Cómo Ejecutar el Proyecto

Tienes dos alternativas para poner en marcha la aplicación en tu entorno local:

### Opción 1: Usando Docker (Recomendado)

Si cuentas con Docker y Docker Compose instalados, puedes ejecutar la aplicación sin configurar un entorno de Python manualmente.

1. Abre una terminal en la raíz del proyecto.
2. Ejecuta el comando:
   ```bash
   docker-compose up --build
   ```
3. Una vez finalizado el proceso de construcción, abre tu navegador e ingresa a:
   [http://localhost:8501](http://localhost:8501)

### Opción 2: Ejecución Manual con Python

Se requiere Python 3.10 o superior instalado en el sistema.

1. Crea un entorno virtual e instálalo:
   ```bash
   python -m venv venv
   ```
2. Activa el entorno virtual:
   - **En Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **En Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación de Streamlit:
   ```bash
   streamlit run app.py
   ```
5. La aplicación se abrirá automáticamente en tu navegador predeterminado (por defecto en `http://localhost:8501`).

---

## 📊 Origen de los Datos (Fuentes Oficiales)

- **Límites Político-Administrativos de Mendoza (Departamentos):** [API de Georef - Argentina.gob.ar](https://apis.datos.gob.ar/georef/api/v2.0/departamentos.geojson?provincia=Mendoza).
- **Establecimientos de Salud (REFES):** [Ministerio de Salud de la Nación - Datos Abiertos](https://datos.salud.gob.ar/dataset/establecimientos-de-salud).
- **Población por Departamento:** Datos definitivos del **Censo Nacional de Población, Hogares y Viviendas 2022 (INDEC)**.
