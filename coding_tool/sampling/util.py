import plotly
import plotly.graph_objs as go

import pandas as pd
import json


def create_plot_pie(c):
    labels = []
    values = []
    for element in c:
        labels.append(element)
        values.append(int(c[element]))
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def create_plot_violin(**set_data):
    data = []
    for key, piece_of_data in set_data.items():
        df = pd.DataFrame({'y': piece_of_data})
        data.append(go.Violin(x=key, y=df['y'], box_visible=True, line_color='black',
                              meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
                              x0=key))
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
