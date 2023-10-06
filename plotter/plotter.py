import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px


class Plotter(object):

    def __init__(self):

        self.traces = dict(
            bar=BarTrace
        )


class Trace(object):
    def __init__(self, data: dict):
        self.data = data

    def build_trace(self):
        ...

class BarTrace(Trace):
    def __init__(self, data):
        super(BarTrace, self).__init__(data)


    def build_trace(self):
        ...


