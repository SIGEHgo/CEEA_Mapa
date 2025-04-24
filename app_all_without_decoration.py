import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash_core_components as dcc
import dash_html_components as html
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

# Carga de datos y definición de variables
shp_municipal = gpd.read_file("./assets/Datos/shp/Historicos_Acciones.shp")
shp_regional = gpd.read_file("./assets/Datos/shp/Regional.shp")
columns_list = shp_municipal.columns.tolist()
opciones_cloro = [col for col in columns_list if 'CLORO' in col]
anios = {i: re.sub(r"CLORO_", "", col) for i, col in enumerate(opciones_cloro)}

map_default_municipal = funciones_auxiliares.generarMapApartirEleccion_Municipal(arhivo_sph=shp_municipal, lista_eleccion=opciones_cloro[-1])
map_default_regional = funciones_auxiliares.generarMapApartirEleccion_Regional(arhivo_sph=shp_regional, lista_eleccion=opciones_cloro[-1])


#########################
### Paleta de colores ###
#########################

# Lógica de renderizado de GeoJSON en JavaScript
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.hideout;
    const value = feature.properties[colorProp];
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];
        }
    }
    return style;
}""")

# Clases para la paleta de colores
classes = [-2, -0.0000000001, 0.199999999999999999, 1.5]
colorscale = ['rgb(205,205,205)', 'rgb(255,0,0)', 'rgb(112,173,71)', 'rgb(255, 192, 0)']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

# Crea colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(
    categories=["No hay dato", "CI < 0.2", "0,2 <= CI <= 1.5", "CI > 1.5"],
    colorscale=colorscale,
    width=300,
    height=30,
    position="bottomleft",
    className="colorbar_custom"
)


#########################################
### Definimos parámetros interactivos ###
#########################################

# Creación de GeoJSON.
geojson = dl.GeoJSON(
    data=map_default_municipal,
    style=style_handle,
    zoomToBounds=True,
    zoomToBoundsOnClick=True,
    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),
    hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="Valor-actual"),
    id="geojson"
)


############################################
### Definición de Componentes del Layout ###
############################################

encabezado = dbc.Row([
    dbc.Col(
        html.H2("Indicadores de Calidad del Agua", style={'color': 'white', 'margin': '0', 'padding': '2vh 0 0 10px'}),
        width=7, xxl=7, xl=7, lg=7, md=7, sm=12, xs=12,
        style={'backgroundColor': 'rgb(157, 36, 73)', 'padding': '0', 'margin': '0'}
    ),
    dbc.Col(
        html.A(
            html.Img(src="./assets/Imagenes/Planeacion_dorado.png", style={'width': '100%', 'height': '70%', 'padding': '1vh 0 0 10px'}),
            href="http://sigeh.hidalgo.gob.mx/",
            target="_blank"
        ),
        width=3, xxl=3, xl=3, lg=3, md=3, sm=7, xs=7,
        style={'backgroundColor': 'rgb(157, 36, 73)', 'padding': '0', 'margin': '0'}
    ),
    dbc.Col(
        html.A(
            html.Img(src="./assets/Imagenes/CEAA_dorado.png", style={'width': '75%', 'height': '75%', 'padding': '1vh 0 0 10px'}),
            href="https://ceaa.hidalgo.gob.mx/",
            target="_blank"
        ),
        width=2, xxl=2, xl=2, lg=2, md=2, sm=5, xs=5,
        style={'backgroundColor': 'rgb(157, 36, 73)', 'padding': '0', 'margin': '0'}
    )
],
    style={"height": "12vh", 'width': '100vw', 'padding': '0', 'margin': '0'}
)




########################
### Botone Laterales ###
########################

layers_icon = html.I(id="layers_icon", className="bi bi-layers", style={'margin': '0', 'paddin': '0'})
search_icon = html.I(id="search_icon", className="bi bi-search", style={'margin': '0', 'paddin': '0'})
information_icon = html.I(id="about_information_icon", className="bi bi-book",  style={'margin': '0', 'paddin': '0'})
question_icon = html.I(id="question_icon", className="bi bi-question-lg",  style={'margin': '0', 'paddin': '0'})


botton_layers = dbc.Button(
    [layers_icon],
    id="botton_layers_icon",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom",
    style={'width': '70%', 'height': '6vh', 'margin': '1vh 10% 1vh 10%'}
)

botton_search = dbc.Button(
    [search_icon],
    id="botton_search_icon",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom",
    style={'width': '70%', 'height': '6vh', 'margin': '1vh 10% 1vh 10%'}
)

botton_information = dbc.Button(
    [information_icon],
    id="botton_information_icon",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom",
    style={'width': '70%', 'height': '6vh', 'margin': '1vh 10% 1vh 10%'}
)

botton_question = dbc.Button(
    [question_icon],
    id="botton_question_icon",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom",
    style={'width': '70%', 'height': '6vh', 'margin': '1vh 10% 1vh 10%'}
)


###########################
### Offcanvas and Modals###
###########################

########################
### OffCanvas Layers ###
########################

botton_municipal = dbc.Button(
    "Municipal",
    id= "botton_municipal",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom active",
    style={'width': '70%', 'height': '6vh', 'margin': '1vh 10% 1vh 10%'}
)

botton_regional = dbc.Button(
    "Regional",
    id= "botton_regional",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom",
    style={'width': '70%', 'height': '6vh', 'margin': '1vh 10% 1vh 10%'}
)

slider_periodo = dcc.Slider(
    id="slider_periodo",
    step=None,
    marks=anios,
    value=list(anios.keys())[-1],
    className="slider-custom"
)

play_pause_icon = html.I(id="play_pause", className="bi bi-play-fill")

botton_time = dbc.Button(
    ["Histórico", play_pause_icon],
    id="botton_time",
    color="primary",
    n_clicks=0,
    size="sm",
    outline=True,
    className="button-custom",
    style={'width': '70%', 'height': '5vh', 'margin': '1vh 10% 1vh 10%'}
)

intervalo_tiempo = dcc.Interval(
    id="intervalo_tiempo",
    interval=2500,  # 1000 = 1s
    n_intervals=2024,  # Valor inicial
    disabled=True
)


offcanvas_layers = html.Div(
    [
        dbc.Offcanvas(
            children=[ 
                html.H5("Tipo de mapa", style={'color': 'black'}),
                html.Div( 
                    children= [ botton_municipal, botton_regional],
                    style={"display": "flex", "justifyContent": "space-around"}
            ),
                html.Br(),
                html.H5("Periodo", style={'color': 'black'}),
                slider_periodo,
                html.Br(),
                html.Br(),
                html.H5("Explora el tiempo", style={'color': 'black'}),
                botton_time,
                intervalo_tiempo
            ],
            id="offcanvas_layers",
            title= html.H4("Capas de información", style={'textAlign': 'center', 'color': 'black'}),
            is_open=False,
            backdrop=False,
            style={"height": "88vh", "marginTop": "12vh", "backgroundColor": " #c1c0c0"}
        ),
    ],
)



########################
### OffCanvas Search ###
########################

municipal_geo = funciones_auxiliares.obtenerCentroides_Municipales(shp_municipal)
regional_geo = funciones_auxiliares.obtenerCentroides_Regionales(shp_regional)

# Dropdown para buscar municipios o regiones según el mapa actual.
buscador = dcc.Dropdown(
    id='buscador',
    options=[{'label': mun, 'value': latitud} for mun, latitud in zip(municipal_geo.NOM_MUN, municipal_geo.latitud)],
    placeholder="Buscar:",
    value=None,
    clearable=False,
    className="buscador_custom"
)

offcanvas_search = html.Div(
    [
        dbc.Offcanvas( 
            children = [
                buscador
            ],
            id="offcanvas_search",
            title= html.H4("Busca tu municipio o región", style={'textAlign': 'center', 'color': 'black'}),
            is_open=False,
            backdrop=False,
            style={"height": "88vh", "marginTop": "12vh", "backgroundColor": " #c1c0c0"},
        ),
    ]
)




modal_information = dbc.Modal( children = 
    [ dbc.ModalHeader(dbc.ModalTitle("Informacion Adicional")),
    dbc.ModalBody("La Norma Oficial Mexicana NOM-127-SSA1-2021 establece que el agua de uso y consumo humano debe presentar una concentración de cloro residual libre entre 0.2 y 1.5mg/L."),
    dbc.ModalFooter(
        dbc.Button("De Acuerdo", id="close_information", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal_information",
    is_open=False,
)

modal_content = [
    dbc.ModalHeader(
        dbc.ModalTitle("Explora el mapa")
    ),
    dbc.ModalBody(
        html.Div([
            html.P(
                "Este mapa web interactivo tiene una barra lateral en la parte izquierda con cuatro secciones principales:"
            ),
            html.Ol([
                html.Li([
                    html.Strong("Capas de Información:"),
                    html.Ul([
                        html.Li("Permite elegir el tipo de mapa a visualizar (municipal o regional)."),
                        html.Li("Incluye una línea de tiempo para seleccionar el año deseado."),
                        html.Li('Tiene un botón "Histórico" que cambia el mapa automáticamente cada 2.5 segundos para mostrar diferentes periodos.')
                    ])
                ]),
                html.Li([
                    html.Strong("Buscador:"),
                    html.Ul([
                        html.Li("Facilita buscar un municipio o una región, según el mapa que estés viendo."),
                        html.Li("Al buscar, el mapa se centra en el área seleccionada.")
                    ])
                ]),
                html.Li([
                    html.Strong("Información Adicional:"),
                    html.P("Ofrece detalles y explicaciones más específicas sobre los indicadores mostrados.")
                ]),
                html.Li([
                    html.Strong("Explora el Mapa:"),
                    html.P("Es la opción que has seleccionado para interactuar directamente con el mapa.")
                ])
            ]),
            html.P("Cada sección está diseñada para que puedas navegar y obtener la información que necesites de manera sencilla y visual.")
        ])
    )
]

modal_question = dbc.Modal(
    children=[
        *modal_content,
        dbc.ModalFooter(
            dbc.Button("De Acuerdo", id="close_question", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal_question",
    is_open=False,
)

##################################
### Barra vertical interactiva ###
##################################

vertical_nav = dbc.Nav(
    [
        dbc.NavLink(children = botton_layers, id="layers_nav", style = {'margin': '0', 'padding': '0'}),
        dbc.NavLink(children = botton_search, id="search_nav", style = {'margin': '0', 'padding': '0'}),
        dbc.NavLink(children = botton_information, id="information_nav", style = {'margin': '0', 'padding': '0'}),
        dbc.NavLink(children = botton_question, id="question_nav", style = {'margin': '0', 'padding': '0'}),
    ],
    vertical=True,
    pills=True,
    style={
        "height": "100vh",
        'width': '6vw',
        "padding": "0",
        'margin': '0',
        'backgroundColor': 'rgb(179, 142, 93)'
    }
)


###############
### Lateral ###
###############

barra_lateral = html.Div(
    children= vertical_nav,
    id="barra_lateral",
    className="barra_lateral",
    style={
        "position": "absolute",
        "backgroundColor": "black",
        "height": "100vh", 
        'width': '6vw',
        "zIndex": "1000"
    }
)

# Mapa
mapa = dbc.Row(
    children=[
        dbc.Col(
            dl.Map(
                id="mapa",  # Id asignado para usar en callbacks
                children=[
                    dl.TileLayer(),
                    dl.ZoomControl(position="topright"),
                    geojson,
                    barra_lateral,
                ],
                center=[20, -98], 
                zoom=6,
                zoomControl=False, 
                style={'height': '88vh'}
            ),
            width=12, xxl=12, xl=12, lg=12, md=12, sm=12, xs=12,
            style={'backgroundColor': '#000000', 'padding': '0', 'margin': '0'}
        )
    ],
    style={"height": "88vh", 'width': '100vw', 'padding': '0', 'margin': '0'}
)



##############
### Layout ###
##############

app = Dash(
    prevent_initial_callbacks=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP]
)
app.layout = dbc.Container([
    encabezado,
    mapa,
    offcanvas_layers,
    offcanvas_search,
    modal_information,
    modal_question,
    dcc.Store(id="current_map", data="municipal")
],
    fluid=True,
    style={'height': '100vh', 'width': '100vw', 'padding': '0', 'margin': '0'}
)


#####################################
### CallBacks Model and OffCanvas ###
######################################


### offcanvas_layers
@app.callback(
    Output("offcanvas_layers", "is_open"),
    [Input("botton_layers_icon", "n_clicks")],
    [State("offcanvas_layers", "is_open")]
)
def offcanvas_layers_open(n1, is_open):
    if n1:
        return not is_open
    return is_open


### offcanvas_search
@app.callback(
    Output("offcanvas_search", "is_open"),
    [Input("botton_search_icon", "n_clicks")],
    [State("offcanvas_search", "is_open")]
)
def offcanvas_layers_open(n1, is_open):
    if n1:
        return not is_open
    return is_open

### modal_information
@app.callback(
    Output("modal_information", "is_open"),
    [Input("botton_information_icon", "n_clicks"), Input("close_information", "n_clicks")],
    [State("modal_information", "is_open")]
)
def modal_information_open(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


### modal_question
@app.callback(
    Output("modal_question", "is_open"),
    [Input("botton_question_icon", "n_clicks"), Input("close_question", "n_clicks")],
    [State("modal_question", "is_open")]
)
def modal_question_open(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



# Callback para cambiar el mapa entre municipal y regional ademas de cambiar el color del botón activo
@app.callback(
    [
        Output("geojson", "data", allow_duplicate=True),
        Output("current_map", "data"),
        Output("botton_municipal", "className"),
        Output("botton_regional", "className"),
        Output("buscador", "options")
    ],
    [
        Input("botton_municipal", "n_clicks"),
        Input("botton_regional", "n_clicks")
    ],
    State("current_map", "data"),
    prevent_initial_call=True  # evita que se dispare automáticamente al cargar
)
def toggle_active(mun_clicks, reg_clicks, current_map):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    clicked = ctx.triggered[0]["prop_id"].split(".")[0]

    if clicked == "botton_municipal":
        # Se genera el mapa para el caso municipal
        new_data = funciones_auxiliares.generarMapApartirEleccion_Municipal(
            arhivo_sph=shp_municipal, lista_eleccion=opciones_cloro[-1]
        )
        opciones = [{'label': mun, 'value': latitud} 
                    for mun, latitud in zip(municipal_geo.NOM_MUN, municipal_geo.latitud)]
        return new_data, "municipal", "button-custom active", "button-custom", opciones

    elif clicked == "botton_regional":
        # Se genera el mapa para el caso regional
        new_data = funciones_auxiliares.generarMapApartirEleccion_Regional(
            arhivo_sph=shp_regional, lista_eleccion=opciones_cloro[-1]
        )
        opciones = [{'label': mun, 'value': lat} 
                    for mun, lat in zip(regional_geo.Región, regional_geo.latitud)]
        return new_data, "regional", "button-custom", "button-custom active", opciones

    raise PreventUpdate




# Callback para actualizar el mapa según el slider
@app.callback(
    Output("geojson", "data", allow_duplicate=True),
    [Input("slider_periodo", "value")],
    State("current_map", "data"),
    prevent_initial_call=True
)
def actualizar_mapa_por_slider(indice, current_map):
    columna = opciones_cloro[indice]
    if current_map == "municipal":
        map_default = funciones_auxiliares.generarMapApartirEleccion_Municipal(
            arhivo_sph=shp_municipal, lista_eleccion=columna)
    else:
        map_default = funciones_auxiliares.generarMapApartirEleccion_Regional(
            arhivo_sph=shp_regional, lista_eleccion=columna)
    return map_default



# Callback para hacer que funcione el botón de play/pause y el intervalo de tiempo
@app.callback(
    [Output("intervalo_tiempo", "disabled"),
     Output("play_pause", "className"),
     Output("botton_time", "className")],  
    [Input("botton_time", "n_clicks"),
     Input("botton_time", "className")],
    State("intervalo_tiempo", "disabled")
)
def intervalo_tiempo_activar_desactivar(numero_clicks, disabled, clase):
    print(f"Clicks: {numero_clicks}, Disabled: {disabled}")
    if not numero_clicks or numero_clicks == 0:
        return True, "bi bi-play-fill", "button-custom"  
    if numero_clicks % 2 == 1:
        return False, "bi bi-pause-fill", "button-custom active"  
    else:
        return True, "bi bi-play-fill", "button-custom"  


# Callback para mover el slider automáticamente
@app.callback(
    Output("slider_periodo", "value"),
    Input("intervalo_tiempo", "n_intervals"),
    State("slider_periodo", "value")
)
def moverse_automaticamente(n_intervals, valor_actual):
    total_anios = len(opciones_cloro)
    nuevo_valor = (valor_actual + 1) % total_anios
    return nuevo_valor


# Callback para centrar el mapa al seleccionar un municipio o región desde el dropdown
@app.callback(
    [Output("mapa", "center"),
     Output("mapa", "zoom")],
    Input("buscador", "value"),
    State("current_map", "data")
)
def update_map(latitud, current_map):
    if current_map == "municipal":
        if latitud is None:
            raise PreventUpdate
        else:
            # Filtra el DataFrame para encontrar el municipio seleccionado
            municipio = municipal_geo[municipal_geo["latitud"] == latitud]
            
            # Extrae la Longitud del municipio seleccionado y conviértelo a un valor único
            longitud = municipio["longitud"]
            
            if longitud is None:
                raise PreventUpdate
            
    else:
        if latitud is None:
            raise PreventUpdate
        else:
            # Filtra el DataFrame para encontrar el municipio seleccionado
            municipio = regional_geo[regional_geo["latitud"] == latitud]
            
            # Extrae la Longitud del municipio seleccionado y conviértelo a un valor único
            longitud = municipio["longitud"]
            
            if longitud is None:
                raise PreventUpdate
            
        # Actualiza el mapa con la nueva ubicación
    return [latitud, longitud], 10

#################
### Copilador ###
#################

if __name__ == '__main__':
    app.run(debug=True)
