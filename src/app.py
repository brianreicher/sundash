from dash import Dash, html, dcc, Input, Output
from components import *

# build app
app = Dash(__name__)
app.layout = html.Div([
    html.H1('SunDash - an interactive UI for observing & analyzing solar activity'),
    dcc.Graph(id='graph', style={'width': '100vw', 'height': '50vh'}),
    html.P('Select Phenomena'),
    dcc.Dropdown(id='phenomena', options=['sunspots', 'solar flares'], value='sunspots', clearable=False),
    dcc.Slider(id='smmoothing', min=1, max=10, step=1, value=3),
])


# decorators, object and specific attribute
@app.callback(Output('graph', 'figure'),
              Input('phenomena', 'value'),
              Input('smoothing', 'value'),
              Input('prune', 'value'))
def display_sankey(phenotype, min_pubs, prune):
    pass


app.run_server(debug=True)