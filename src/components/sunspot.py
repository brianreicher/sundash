"""
File: sunspot.py

Description: component class for processing & plotting sunspot data
"""

import plotly.express as px
import pandas as pd

from base_component import BaseComponent


class SunSpot(BaseComponent):
    def __init__(self):
        super().__init__()

    def load_data(self) -> None:
        pass



