import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash_core_components as dcc
import dash_bootstrap_components as dbc  # Importa Dash Bootstrap Components
from dash import Dash, html, Output, Input, State, no_update
import rasterio
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from rasterio.warp import transform_bounds
import os
import re
from dash_extensions.javascript import arrow_function, assign
import geopandas as gpd
import funciones_auxiliares
from funciones_auxiliares import generarMapApartirEleccion_Municipal, generarMapApartirEleccion_Regional, obtenerCentroides_Municipales, obtenerCentroides_Regionales
from dash.exceptions import PreventUpdate
from flask import Flask













######################################################
### Definición de los componentes de la aplicación ###
######################################################

# slider_periodo = dcc.Slider(
#     id="slider_periodo",
#     step=None,
#     marks=anios,
#     value=list(anios.keys())[-1],
#     className="slider-custom"
# )





###################################
### Estructura de la aplicación ###
###################################

encabezado =  dbc.Row([
        dbc.Col(
            html.H2("Indicadores de Calidad del Agua", style={'color': 'white', 'margin':'0', 'padding': '2vh 0 0 10px'}), # paddin arriba, derecha abajo izquierda
            width = 7,
            xxl = 7, xl = 7, lg = 7, md = 7, sm = 12,  xs = 12, 
            style = {'backgroundColor': '#9C2448', 'padding': '0','margin':'0'} 
        ),
        dbc.Col(
            #html.H2("Barra", style={'color': 'white', 'margin':'0', 'padding': '0'}),
            html.A(
                html.Img(src="./assets/Imagenes/Planeacion_dorado.png", style={'width': '100%', 'height': '70%', 'padding': '1vh 0 0 10px'}),
                href = "https://sigeh.hidalgo.gob.mx/", 
                target= "_blank"
            ),
            width = 3,
            xxl = 3, xl = 3, lg = 3, md = 3, sm = 7,  xs = 7, 
            style = {'backgroundColor': '#9C2448', 'padding': '0', 'margin':'0'}
        ),
        dbc.Col(
            html.A(
                html.Img(src="./assets/Imagenes/CEAA_dorado.png", style={'width': '75%', 'height': '75%', 'padding': '1vh 0 0 10px'}),
                href = "https://ceaa.hidalgo.gob.mx/",
                target= "_blank" 
            ),
            width = 2,
            xxl = 2, xl = 2, lg = 2, md = 2, sm = 5,  xs = 5, 
            style = {'backgroundColor': '#9C2448', 'padding': '0', 'margin':'0'}
        )
    ], 
    style={"height": "12vh", 'width': '100vw' , 'padding':'0', 'margin':'0'}
    )


enmedio = dbc.Row([
    dbc.Col(
        children= html.H2("Barra de tiempo", style={'color': 'white', 'margin':'0', 'padding': '2vh 0 0 10px'}),
        width = 10,
        xxl = 10, xl = 10, lg = 10, md = 10, sm = 10,  xs = 10, 
        style = {'backgroundColor': '#BC955B', 'padding': '0','margin':'0'} 
    ),
    dbc.Col(
        children= html.H2("Botones", style={'color': 'black', 'margin':'0', 'padding': '2vh 0 0 10px'}),
        width = 2,
        xxl = 2, xl = 2, lg = 2, md = 2, sm = 2,  xs = 2, 
        style = {'backgroundColor': "#FFFFFF", 'padding': '0','margin':'0'} 
    )
], style={"height": "8vh", 'width': '100vw' , 'padding':'0', 'margin':'0'}
)   


mapa = dbc.Row(
    dbc.Col(
        html.Iframe(src="assets/Datos/Mapas/Mapa_2023.html", style={'width': '95%', 'height': '', 'border': '0', 'padding': '0', 'margin': '0'}),
        
        # dl.Map(children= [dl.TileLayer()],
        #         center=[20, -98],
        #         zoom=6,
        #         style={'height': '80vh'}),
        width = 12,
        xxl = 12, xl = 12, lg = 12, md = 12, sm = 12,  xs = 12, 
        style = {'backgroundColor': '#000000', 'padding': '0','margin':'0'} 
    ),
    style={"height": "80vh", 'width': '100vw' , 'padding':'0', 'margin':'0'}
)



server = Flask(__name__)

app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP,"assets/Style.css"],)

app.layout = dbc.Container([
    encabezado,
    enmedio,
    mapa
],
    fluid=True,
    style={'height': '100vh', 'width': '100vw', 'padding': '0', 'margin': '0'}
)




#################
### Copilador ###
#################

if __name__ == '__main__':
    app.run(debug=True)
