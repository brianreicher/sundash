"""
File: sunspot.py

Description: component class for processing & plotting sunspot data
"""

import plotly.express as px
import pandas as pd


class SunSpot:

    def __init__(self, year_range: list, smooth_val):
        self.year_range = year_range
        self.smooth = smooth_val
        self.year_data = pd.read_csv('../../data/SN_m_tot_V2.0.csv', sep=';')

        self.cleaned = False

    def clean_data(self) -> None:
        df = self.year_data
        df.columns = ['year', 'month', 'year_month', 'nspots', 'null', 'null', 'null']
        df = df[(df.year_month > float(self.year_range[0])) & (df.year_month < float(self.year_range[1]))]
        self.year_data = df
        self.cleaned = True

    def plot_data(self):
        if self.cleaned is False:
            self.clean_data()

        fig = px.line(self.year_data, x="year_month", y="nspots", title='Sunspots Per Year')
        return fig




