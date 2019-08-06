import plotly
import plotly.graph_objs as go

import pandas as pd
import json

colors = ['lightseagreen', 'lightsalmon', 'lightsteelblue',
          'lightcoral', 'lightgoldenrodyellow', 'lime']


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


def create_plot_violin(dic_data):
    data = []
    counter = 0
    for key, piece_of_data in dic_data.items():
        df = pd.DataFrame({'y': piece_of_data})
        total = 0
        for data_point in piece_of_data:
            total += data_point
        print(f"key={key}")
        print(f"piece_of_data={piece_of_data}")
        data.append(go.Violin(y=df['y'], box_visible=True, line_color='black',
                              meanline_visible=True, fillcolor=colors[counter], opacity=0.6,
                              x0=f"total={total}", name=key))
        counter += 1
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
