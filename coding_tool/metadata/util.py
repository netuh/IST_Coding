import plotly
import plotly.graph_objs as go

import pandas as pd
import json


def create_plot(c):
    x = []
    y = []
    for element in c:
        x.append(element)
        y.append(c[element])
    df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
    data = [
        go.Bar(
            # marker_color='indianred',
            x=df['x'],  # assign x as the dataframe column 'x'
            y=df['y']

        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
