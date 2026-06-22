import os
import ssl
import requests
import urllib3
import pandas as pd
import geopandas as gpd

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

POPULATION_DATA = {
    "Capital": 115041,
    "General Alvear": 46412,
    "Godoy Cruz": 195183,
    "Guaymallén": 321966,
    "Junín": 43512,
    "La Paz": 12086,
    "Las Heras": 234401,
    "Lavalle": 48123,
    "Luján de Cuyo": 172108,
    "Maipú": 219402,
    "Malargüe": 32105,
    "Rivadavia": 61205,
    "San Carlos": 38102,
    "San Martín": 125102,
    "San Rafael": 215020,
    "Santa Rosa": 18105,
    "Tunuyán": 56102,
    "Tupungato": 41205
}

def get_data_dir():
    """Devuelve la ruta al directorio de datos."""
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def load_departments():
    """Carga los departamentos de la provincia de Mendoza desde el GeoJSON."""

    data_dir = get_data_dir()
    local_path = os.path.join(data_dir, "mendoza_departments.geojson")
    
    if os.path.exists(local_path):
        return gpd.read_file(local_path)
    
    url = "https://apis.datos.gob.ar/georef/api/v2.0/departamentos.geojson?provincia=Mendoza"
    response = requests.get(url, verify=False)
    response.raise_for_status()
    geojson_data = response.json()
    
    gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
    gdf.crs = "EPSG:4326"
    gdf.to_file(local_path, driver="GeoJSON")
    return gdf

def load_health_centers():
    """Carga los centros de salud de la provincia de Mendoza desde el CSV."""

    data_dir = get_data_dir()
    local_path = os.path.join(data_dir, "mendoza_health_centers.csv")
    
    if os.path.exists(local_path):
        return pd.read_csv(local_path)
    
    url = "https://datos.salud.gob.ar/dataset/336cf4d9-447a-44c4-8e34-0ba1fc293d55/resource/6aa2c00e-0706-4d39-bade-95ceb271a4c6/download/establecimientos-asistenciales-asentados-registro-federal-refes-20251215.csv"
    
    df = pd.read_csv(url, low_memory=False)
    
    df_mendoza = df[df["provincia_nombre"].str.lower() == "mendoza"].copy()
    
    df_mendoza["longitud"] = pd.to_numeric(df_mendoza["longitud"], errors="coerce")
    df_mendoza["latitud"] = pd.to_numeric(df_mendoza["latitud"], errors="coerce")
    df_mendoza = df_mendoza.dropna(subset=["longitud", "latitud"])
    
    df_mendoza.to_csv(local_path, index=False)
    return df_mendoza
