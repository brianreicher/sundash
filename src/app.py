from dash import Dash, html, dcc, Input, Output
from components import sunspot

# build app
app = Dash(__name__)

colors = {
    'background': '#DEEA6B',
    'text': '#7FDBFF'}

app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[html.H1('SunDash - an interactive UI for observing & analyzing solar activity'),
                                dcc.Graph(id='years_graph'),
                                html.P('Select Year Range'),
                                dcc.RangeSlider(1749, 2000, 1, value=[1850, 1900], marks={1750: '1750', 1800: '1800',
                                                                                          1850: '1850', 1900: '1900',
                                                                                          1950: '1950', 2000: '2000'},

                                                tooltip={"placement": "bottom", "always_visible": True},
                                                id='range_slider'),
                                html.P('Select Smoothing Factor'),
                                dcc.RadioItems(options=['Daily Running Average', 'Yearly Average',
                                                        '13-month Smoothed Total'],
                                               value='Daily Running Average', id='smooth_button'),
                                dcc.Graph(id='variability_graph'),
                                html.P('Select Variability Period'),
                                dcc.Slider(1, 20, 1, value=11, id='var_slider'),    
                                html.Br(),
                                html.P('RealTime NASA Sun Images'),
                                html.Img(id='sun_img'),
                                html.Button(id='update_button')
                                ]
                      )


@app.callback(Output('years_graph', 'figure'),
              Input('range_slider', 'value'),
              Input('smooth_button', 'value'),
              )
def update_activity_plot(years: list, smoothing: str):
    sun = sunspot.SunSpot(year_range=years, smooth_index=smoothing)
    return sun.plot_sunspot_trends()


@app.callback(Output('variability_graph', 'figure'),
              Input('range_slider', 'value'),
              Input('var_slider', 'value'))
def update_var_plot(years: list, var: int):
    sun = sunspot.SunSpot(year_range=years, period=var)
    return sun.plot_sunspot_variability()


@app.callback(Output('sun_img', 'image'),
              Input('update_button', 'n_clicks'))
def grab_sun_img():
    pass


app.run_server(debug=True)
