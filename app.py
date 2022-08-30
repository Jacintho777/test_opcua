from dash import Dash,html,dcc
from dash.dependencies import Input, Output
from client_prod_simul_test import *

app = Dash(__name__)

server = app.server

app.layout = html.Div(
            children = [
                dcc.Interval(id = 'grph_interval',interval = 7000, n_intervals=0), #intervall must be set on the tempo of the database growth
                html.H1('OPC-UA appTest',style={'text-align':'center'}),
                dcc.Graph(id = 'grph',style = {'margin-left':'20rem','margin-right':'20rem'}),
            ]
)

@app.callback(
    Output('grph','figure'),

    Input('grph_interval','n_intervals'),
)

def update(n_intervals):
    
    return update_plots()

if __name__ == '__main__':

    app.run_server(debug = True)