from dash import Dash, html, dcc, Input, Output
import sunspot

# build app, server for heroku
app = Dash(__name__)
server = app.server

# set app background color
colors = {
    'background': '#DEEA6B'}


# apply HTML layout
app.layout = html.Div(style={'backgroundColor': colors['background']},
                      children=[html.H1('SunDash - an Interactive UI for Observing & Analyzing solar activity'),
                                html.H3('Sunspots Measured per Year'),
                                # base graph, sunspots over time
                                dcc.Graph(id='years_graph'),
                                html.P('Select Year Range'),
                                dcc.RangeSlider(1749, 2000, 1, value=[1850, 1900], marks={1750: '1750', 1800: '1800',
                                                                                          1850: '1850', 1900: '1900',
                                                                                          1950: '1950', 2000: '2000'},

                                                tooltip={"placement": "bottom", "always_visible": True},
                                                id='range_slider'),
                               
                                # smoothing for base plot
                                html.P('Select Smoothing Factor'),
                                dcc.Dropdown(['Daily Running Average (no data before 1820)', 'Yearly Average',
                                                        '13-month Smoothed Total'],
                                               value='Daily Running Average (no data before 1820)', id='smooth_button'),
                                
                                # sunspot variabilitygraph
                                dcc.Graph(id='variability_graph'),
                                html.P('Select Variability Period'),
                                dcc.Slider(1, 20, 1, value=11, id='var_slider'),    
                                html.Br(),

                                # realtime NASA solar images
                                html.Div(children=[
                                html.H3('RealTime NASA Sun Images: SDO/HMI Continuum, SDO HMI Magnetogram, SOHO EIT 171'),
                                html.Img(id='continuum', src='https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg',
                                        width=300, height=300),
                                html.Img(id='magetogram', src='https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg', 
                                width=300, height=300),
                                html.Img(id='SOHO EIT 171', src='https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg', width=300, height=300)
                                ])
                                ]
                      )


# callback func for base plot
@app.callback(Output('years_graph', 'figure'),
              Input('range_slider', 'value'),
              Input('smooth_button', 'value'),
              )
def update_activity_plot(years: list, smoothing: str):
    sun = sunspot.SunSpot(year_range=years, smooth_index=smoothing)
    return sun.plot_sunspot_trends()

# calback func for variability plot
@app.callback(Output('variability_graph', 'figure'),
              Input('range_slider', 'value'),
              Input('var_slider', 'value'))
def update_var_plot(years: list, var: int):
    sun = sunspot.SunSpot(year_range=years, period=var)
    return sun.plot_sunspot_variability()


# run to localhost
app.run_server(debug=True)
