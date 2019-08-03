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
    # df1 = pd.DataFrame({'y': set_data[0]})
    # df2 = pd.DataFrame({'y': set_data[1]})
    # df3 = pd.DataFrame({'y': set_data[1]})
    # data = [
    #     go.Violin(y=df3['y'], box_visible=True, line_color='black',
    #               meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
    #               x0='Student'),
    #     go.Violin(y=df2['y'], box_visible=True, line_color='black',
    #               meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
    #               x0='Professinals'),
    #     go.Violin(y=df1['y'], box_visible=True, line_color='black',
    #               meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
    #               x0='Total')
    # ]
    data = []
    for key, piece_of_data in set_data.items():
        df = pd.DataFrame({'y': piece_of_data})
        data.append(go.Violin(y=df['y'], box_visible=True, line_color='black',
                              meanline_visible=True, fillcolor='lightseagreen', opacity=0.6,
                              x0=key))
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
