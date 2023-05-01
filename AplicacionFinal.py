import os
import base64

import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import dash_bio

from layout_helper import run_standalone_app

import requests


def description():
    return 'Herramienta Automática de Resúmenes.'


def header_colors():
    return {
        'bg_color': '#0D76BF',
        'font_color': '#fff',
        'light_logo': True
    }


def layout():
    return html.Div(id='mhp-page-content', className='app-body', children=[
        dcc.Loading(parent_className='dashbio-loading', children=html.Div(
            id='mhp-graph-div',
        )),
        
        html.Div(id='manhattan-control-tabs', className='control-tabs', children=[
            dcc.Tabs(id='manhattan-tabs', value='what-is', children=[
                dcc.Tab(
                    label='About',
                    value='what-is',
                    children=html.Div(className='control-tab', children=[
                        html.H4(className='what-is', children='Descripción Herramienta'),
                        html.P('Esta herramienta hace uso de técnicas de Machine Learning '
                               'y de inteligencia artificial para clasificar reseñas de peliculas '
                               'de manera automática y en segundos. '
                               'La herramienta tiene como próposito clasificar reseñas de manera muy rápida y eficiente. '
                               ),
                        html.Br(), html.Br(),
                        html.Img(
                            src='data:image/png;base64,{}'.format(
                                base64.b64encode(
                                    open(
                                        './assets/pelicula.png', 'rb'
                                    ).read()
                                ).decode()
                            ),
                            style = {'width': '50%'}
                        )
                    ], style = {"textAlign": "center"})
                    
                ),
                dcc.Tab(
                    label='Clasificar',
                    value='voz',
                    children=html.Div(className='control-tab', children=[
                        html.H4(className='what-is', children='Clasificar Reseña'),
                        html.P('En este paso el modelo tomará la reseña escrita en la caja de texto y la clasificara como positiva o negativa de manera automática. ',
                               style = {"textAlign": "center"}),
                        html.Br(),
                        dcc.Textarea(id="textbox",
                                    style={
                                        'width': '100%',
                                        'height': '150px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    },),
                        html.Br(),
                        html.Button('Clasificar', id='clasificar', n_clicks=0, 
                                    style={
                                        'width': '100%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px'
                                    })
                    ])
                ),
            ])
        ]),
        
        
        html.Div( 
                 children=[html.Br(),
                           html.Div(id='out_texto', style={'textAlign': 'center'})
                           ]
                 )
    ])


def callbacks(_app):
    @_app.callback(
        Output(component_id='out_texto', component_property='children'),
        Input('clasificar', 'n_clicks'),
        State('textbox', 'value')
        
    )
    def update_texto(n_clicks, value):
        if n_clicks != 0:
            
            url = 'http://127.0.0.1:8000/predict/'
            myobj = {'descripcion': value}
            
            x = requests.post(url, json = myobj)
            
            resp = "Positiva!"
            
            if "positivo" in x.text:
                resp = "Positiva!"
            else:
                resp = "Negativa!"
        
            return html.Div(children=[html.Br(),html.Br(),
                                  html.B("Reseña Clasificada"),
                                      html.P(value),
                                      html.Br(), html.Br(),
                                      html.B("Clasificacion"),
                                      html.Br(),
                                      html.P(resp),
                                      html.Br(),]
                            )

app = run_standalone_app(layout, callbacks, header_colors, __file__)
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)