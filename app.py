#! C:/Users/mpete/AppData/Local/Programs/Python/Python38-32/python

from dash import Dash,html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from client_prod_simul_test import *

app = Dash(__name__)

server = app.server

app.layout = html.Div(
            children = [
                dbc.Row([
                dcc.Interval(id = 'grph_interval',interval = 7000, n_intervals=0), #intervall must be set on the tempo of the database growth
                dbc.Col(lg = 2),
                dbc.Col([
                dbc.Row([html.H1('OPC-UA appTest',style={'text-align':'center'})]),
                dbc.Row([dcc.Graph(id = 'grph')]),
                ],lg  = 8
                ),
                dbc.Col(lg = 2)
                ]
)]
)

@app.callback(
    Output('grph','figure'),

    Input('grph_interval','n_intervals'),
)

def update(n_intervals):
    
    return update_plots()

if __name__ == '__main__':

    app.run_server(debug = True,host = '192.168.11.110',port = 8001)