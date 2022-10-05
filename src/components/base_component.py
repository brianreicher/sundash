"""
File: base_component.py

Description: dash component class, use for abstraction
"""

import plotly.express as px
import pandas as pd


class BaseComponent():
    def __init__(self, **kwargs):
        self.data_loader = getattr(pd, kwargs)

    def load_data(self):
        pass

    def plot_data(self):
        pass


