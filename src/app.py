from dash import Dash, html, dcc, Input, Output
from components import *

# build app
app = Dash(__name__)
app.layout = html.Div([
    html.H1('SunDash - an interactive UI for observing & analyzing solar activity'),
    dcc.Graph(id='graph', style={'width': '100vw', 'height': '50vh'}),
    html.P('Select Phenotype'),
    dcc.Dropdown(id='phenotype', options=['sunspots', 'solar flares'], value='sunspots', clearable=False),
    html.P('Select minimum # of confirming publications'),
    dcc.Slider(id='min_pubs', min=1, max=10, step=1, value=3),
    html.P('Do you want to prune phenotypes to only one gene?'),
    dcc.RadioItems(id='prune', options=["YES", 'NO'], value='YES', inline=True)
])


# decorators, object and specific attribute
@app.callback(Output('graph', 'figure'),
              Input('phenotype', 'value'),
              Input('min_pubs', 'value'),
              Input('prune', 'value'))
def display_sankey(phenotype, min_pubs, prune):
    pass


app.run_server(debug=True)