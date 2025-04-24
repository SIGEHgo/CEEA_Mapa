import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign

import geopandas as gpd
import pandas as pd

def generarMapApartirEleccion_Municipal(arhivo_sph, lista_eleccion):
    arhivo_sph["Valor-actual"] = arhivo_sph[lista_eleccion]
    geojson_data = {
        "type": "FeatureCollection",        # Dices que es geojson
        "features": [                       # Lista de los objetos
            {
                "type": "Feature",                  # Cada objeto que se vaya creando es de ese tipo
                "geometry": feature["geometry"],    # Le pone la geometria
                "properties": {                     # Cada objeto va ha tener propiedades
                    **feature["properties"],        # Pasa por filas
                    "tooltip": f"Municipio: <b>{feature['properties'].get('NOM_MUN','N/A')}</b> ", # Pasar Mouse por encima, le puedo agragar un popup,
                    "popup": (f"Municipio: <b>{feature['properties'].get('NOM_MUN','N/A')}</b><br>"
                              f"CI: <b> {round(feature['properties'].get('Valor-actual'), 2) if feature['properties'].get('Valor-actual') != -1 else 'No hay dato'} mg/L</b> ")
                }
            }
            for idx, feature in enumerate(arhivo_sph.__geo_interface__["features"])        # map_ es del tipo geopandas
        ]
    }
    return geojson_data



def generarMapApartirEleccion_Regional(arhivo_sph, lista_eleccion):
    arhivo_sph["Valor-actual"] = arhivo_sph[lista_eleccion]
    geojson_data = {
        "type": "FeatureCollection",        # Dices que es geojson
        "features": [                       # Lista de los objetos
            {
                "type": "Feature",                  # Cada objeto que se vaya creando es de ese tipo
                "geometry": feature["geometry"],    # Le pone la geometria
                "properties": {                     # Cada objeto va ha tener propiedades
                    **feature["properties"],        # Pasa por filas
                    "tooltip": f"Región: <b>{feature['properties'].get('Región','N/A')}</b>", # Pasar Mouse por encima, le puedo agragar un popup
                    "popup": (f"Región: <b>{feature['properties'].get('Región','N/A')}</b><br>"
                              f"CI: <b>{round(feature['properties'].get('Valor-actual'), 2) if feature['properties'].get('Valor-actual') != -1 else 'No hay dato'} mg/L </b>")
                }
            }
            for idx, feature in enumerate(arhivo_sph.__geo_interface__["features"])        # map_ es del tipo geopandas
        ]
    }
    return geojson_data



def obtenerCentroides_Municipales(shp):
    # Filtrar solo las columnas necesarias
    municipal_geometrias = shp[['NOM_MUN', 'geometry']].copy()

    # Asegurar que la geometría está en EPSG:3857
    if municipal_geometrias.crs != "EPSG:3857":
        municipal_geometrias = municipal_geometrias.to_crs(epsg=3857)

    # Obtener centroides proyectados y convertir a lat/lon
    municipal_geometrias["centroide"] = (
        municipal_geometrias.geometry.centroid.to_crs(epsg=4326)
    )

    # Extraer latitud y longitud
    municipal_geometrias["longitud"] = municipal_geometrias["centroide"].x
    municipal_geometrias["latitud"] = municipal_geometrias["centroide"].y

    # Eliminar la columna de geometría si ya no es necesaria
    municipal_geometrias = municipal_geometrias.drop(columns=["centroide"])
    municipal_geometrias = municipal_geometrias.drop(columns=["geometry"])

    return municipal_geometrias


def obtenerCentroides_Regionales(shp):
    # Filtrar solo las columnas necesarias
    regional_geometrias = shp[['Región', 'geometry']].copy()

    # Asegurar que la geometría está en EPSG:3857
    if regional_geometrias.crs != "EPSG:3857":
        regional_geometrias = regional_geometrias.to_crs(epsg=3857)

    # Obtener centroides proyectados y convertir a lat/lon
    regional_geometrias["centroide"] = (
        regional_geometrias.geometry.centroid.to_crs(epsg=4326)
    )

    # Extraer latitud y longitud
    regional_geometrias["longitud"] = regional_geometrias["centroide"].x
    regional_geometrias["latitud"] = regional_geometrias["centroide"].y

    # Eliminar la columna de geometría si ya no es necesaria
    regional_geometrias = regional_geometrias.drop(columns=["centroide"])
    regional_geometrias = regional_geometrias.drop(columns=["geometry"])

    return regional_geometrias