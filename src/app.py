from dash import Dash, html, dcc, Input, Output
from components import sunspot

# build app
app = Dash(__name__)
app.layout = html.Div([
    html.H1('SunDash - an interactive UI for observing & analyzing solar activity'),
    dcc.Graph(id='graph'),
    html.P('Select Year Range'),
    dcc.RangeSlider(1750, 2000, 1, value=[1800, 190], id='range-slider'),
])


# decorators, object and specific attribute
@app.callback(Output('graph', 'figure'),
              Input('range-slider', 'value'))
def update_line_plot(years: list):
    sun = sunspot.SunSpot(year_range=years, smooth_val=None)
    return sun.plot_data()


app.run_server(debug=True)
