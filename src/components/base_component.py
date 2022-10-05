"""
File: base_component.py

Description: dash component class, use for abstraction
"""

import plotly.express as px
import pandas as pd


class BaseComponent():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def load_data(self):
        pass

    def plot_data(self):
        pass


