from turtle import width
from dash import Dash, html, dcc, Input, Output
from components import sunspot, image_reader

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
                                dcc.Dropdown(['Daily Running Average (no data before 1820)', 'Yearly Average',
                                                        '13-month Smoothed Total'],
                                               value='Daily Running Average (no data before 1820)', id='smooth_button'),
                                dcc.Graph(id='variability_graph'),
                                html.P('Select Variability Period'),
                                dcc.Slider(1, 20, 1, value=11, id='var_slider'),    
                                html.Br(),
                                html.P('RealTime NASA Sun Images'),
                                html.Img(id='sun_img', src='https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg',
                                        width=200),
                                dcc.Dropdown(['SDO/HMI Continuum', 'SDO HMI Magnetogram', 'SOHO EIT 171'], value='SDO/HMI Continuum', 
                                id='img_dropdown')
                                # html.Button(id='update_button', value='Update Images')
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


@app.callback(Output('sun_img', 'src'),
              Input('img_dropdown', 'value'))
def grab_sun_img(img_name) -> None:
    return image_reader.ImageReader(img_name).set_im_link()


app.run_server(debug=True)
