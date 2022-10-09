"""
File: base_component.py

Description: dash component class, use for abstraction
"""


class BaseComponent:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def load_data(self):
        pass

    def plot_data(self):
        pass


