"""
File: sunspot.py

Description: component class for processing & plotting sunspot data
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class SunSpot:
    """
        Class for cleaning and visualizing sunspot data
    """

    def __init__(self, year_range=None, smooth_index=None, period=None):
        # user selected year range slider
        self.year_range = year_range

        # in-depth year data (month average)
        self.year_data = pd.read_csv('../data/SN_m_tot_V2.0.csv', sep=';')
        # set column names
        self.year_data.columns = ['year', 'month', 'decimal_year', 'nspots', 'std', 'ignore', 'ignore']

        # smoothing data
        # daily numbers, to calculate running average
        if smooth_index == 'Daily Running Average (no data before 1820)':
            self.smooth_data = pd.read_csv('../data/SN_d_tot_V2.0.csv', sep=';')
            # set column names
            self.smooth_data.columns = ['year', 'month', 'day', 'decimal_year', 'nspots', 'SNerror', 'Nb observations', 'ignore']
            # use func to set new smoothed_spots col to tbe running mean of daily numbers
            self.smooth_data['smoothed_spots'] = self.smooth_data['nspots'].rolling(100).mean()

        # yearly average smoothed numbers
        elif smooth_index == 'Yearly Average':  # TODO
            self.smooth_data = pd.read_csv('../data/SN_y_tot_V2.0.csv', sep=';')
            # set column names
            self.smooth_data.columns = ['decimal_year', 'smoothed_spots', 'SNerror', 'Nb observations', 'null']

        # 13 month smoothed numbers
        else:
            self.smooth_data = pd.read_csv('../data/SN_ms_tot_V2.0.csv', sep=';')
            # set column names
            self.smooth_data.columns = ['year', 'month', 'decimal_year', 'smoothed_spots', 'SNerror', 'Nb observations', 'ignore']

        # set variability period
        self.period = period

        # checker booleans to see if data is cleaned or grouped
        self.cleaned = False
        self.year_grouped = False

    def clean_data_basic(self, df) -> pd.DataFrame:
        """
            Helper function to preprocess and clean basic sunspot data
        :param df:
            Dataframe on which to preprocess
        :return:
            Preprocessed dataframe
        """
        # eliminate any year values falling outside the user-defined slider year range
        df = df[(df.decimal_year > float(self.year_range[0])) & (df.decimal_year < float(self.year_range[1]))]

        # set cleaned boolean to True and return the cleaned dataframe
        self.cleaned = True
        return df

    def clean_data_variability(self):
        """
            Helper function to apply period grouping on month_avg dataset for variability plot
        
        :return:
            None
        """
        # apply lambda func to send each date measurment to its respective period 
        self.year_data['decimal_year'] = self.year_data['decimal_year'].apply(lambda x: x % self.period)

        # set grouped checker to True
        self.year_grouped = True

    def plot_sunspot_trends(self) -> go.Figure:
        """
            Plots full & smoothed sunspot line plots (Sn vs T)
        :return:
            Plotly.go overlayed figure, with smoothing and nonsmoothed data
        """
        # check to see if data is in the slider range, clean both regular and smooth data and reset cleaned boolean
        if self.cleaned is False:
            self.year_data = self.clean_data_basic(df=self.year_data)
            self.smooth_data = self.clean_data_basic(df=self.smooth_data)
            self.cleaned = False

        # instantiate figure
        fig = go.Figure()

        # create full data plot
        year_plot = go.Line(x=self.year_data["decimal_year"], y=self.year_data["nspots"], name='full_month_avg')

        # create smoothed plot
        smoothed_plot = go.Line(x=self.smooth_data['decimal_year'], y=self.smooth_data['smoothed_spots'], name='smoothed_avg')

        # add overlayed plots to figure
        fig.add_trace(year_plot)
        fig.add_trace(smoothed_plot)

        # set axis labels, legend label, plot title
        fig.update_layout(legend_title_text="Smoothing Levels")
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Number of Sunspots (Sn)")
        fig.update_layout(title_text='Sunspots Over Time', title_x=0.5)

        # return overlayed plot
        return fig

    def plot_sunspot_variability(self):
        """
            Plots variability scatterplot of sunspot data, given a user-defined period
        :return:
            Plotly express scatterplot of variability
        """
        # check for grouping, group if not already and flip checker back to False
        if self.year_grouped is False:
            self.clean_data_variability()
            self.year_grouped: bool = False

        # uses plotly express to dispaly varaibility in sunspot number for said period
        # defined all formatting in-object
        var = px.scatter(data_frame=self.year_data, x='decimal_year', y='nspots',
                         labels={'decimal_year': 'Cycle Num', 'nspots': 'Number of Sunspots (Sn)'},
                         title=f'Sunspot Cycle Variability: Period Length {self.period} years')

        # returns the variability figure
        return var

