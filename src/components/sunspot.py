"""
File: sunspot.py

Description: component class for processing & plotting sunspot data
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class SunSpot:
    """

    """

    def __init__(self, year_range=None, smooth_index=None, period=None):
        self.year_range = year_range

        # in-depth year data (month average)
        self.year_data = pd.read_csv('../data/SN_m_tot_V2.0.csv', sep=';')
        self.year_data.columns = ['year', 'month', 'decimal_year', 'nspots', 'null', 'null', 'null']

        # smoothing
        if smooth_index == 'Daily Running Average (no data before 1820)':
            self.smooth_data = pd.read_csv('../data/SN_d_tot_V2.0.csv', sep=';')
            self.smooth_data.columns = ['year', 'month', 'day', 'decimal_year', 'nspots', 'SNerror', 'Nb observations', 'null']
            self.smooth_data['smoothed_spots'] = self.smooth_data['nspots'].rolling(100).mean()
        elif smooth_index == 'Yearly Average':  # TODO
            self.smooth_data = pd.read_csv('../data/SN_y_tot_V2.0.csv', sep=';')
            self.smooth_data.columns = ['decimal_year', 'smoothed_spots', 'SNerror', 'Nb observations', 'null']
        else:
            self.smooth_data = pd.read_csv('../data/SN_ms_tot_V2.0.csv', sep=';')
            self.smooth_data.columns = ['year', 'month', 'decimal_year', 'smoothed_spots', 'SNerror', 'Nb observations', 'null']

        self.period = period

        self.cleaned = False
        self.year_grouped = False

    def clean_data_basic(self, df) -> pd.DataFrame:
        """

        :param df:
        :return:
        """
        df = df[(df.decimal_year > float(self.year_range[0])) & (df.decimal_year < float(self.year_range[1]))]
        self.cleaned = True
        return df

    def clean_data_variability(self):
        """

        :return:
        """
        if self.cleaned is False:
            self.clean_data_basic(self.year_data)
            self.cleaned = True

        self.year_data['decimal_year'] = self.year_data['decimal_year'].apply(lambda x: x % self.period)
        self.year_grouped = True

    def plot_sunspot_trends(self) -> go.Figure:
        """

        :return:
        """
        if self.cleaned is False:
            self.year_data = self.clean_data_basic(df=self.year_data)
            self.smooth_data = self.clean_data_basic(df=self.smooth_data)
            self.cleaned = False

        fig = go.Figure()
        year_plot = go.Line(x=self.year_data["decimal_year"], y=self.year_data["nspots"], name='year_plot')

        smoothed_plot = go.Line(x=self.smooth_data['decimal_year'], y=self.smooth_data['smoothed_spots'], name='smoothed_plot')

        fig.add_trace(year_plot)
        fig.add_trace(smoothed_plot)
        fig.update_layout(legend_title_text="Temporal Levels")
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Sunspot Number")

        return fig

    def plot_sunspot_variability(self) -> go.Figure:
        """

        :return:
        """
        if self.year_grouped is False:
            self.clean_data_variability()
            self.year_grouped = False

        var = px.scatter(data_frame=self.year_data, x='decimal_year', y='nspots',
                         labels={'decimal_year': 'Cycle Num', 'nspots': 'Sunspot Number'},
                         title=f'Sunspot Cycle: {self.period}')

        return var

