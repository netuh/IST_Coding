from flask import Blueprint, render_template
from coding_tool.models import ExperimentDesign
from coding_tool.util import create_plot_pie, create_plot_bar

from collections import Counter

design = Blueprint('design', __name__)


@design.route("/desings")
def desings():
    desings = ExperimentDesign.query.all()
    word_list = []
    c = Counter()
    c2 = Counter()
    for a_desing in desings:
        word_list.append(a_desing.design.strip().lower())
        c2.update([a_desing.factor_quantity])
    c.update(word_list)
    pie = create_plot_pie(c)
    bar = create_plot_bar(c2)
    print('here')
    return render_template('desings.html', plotDesign=pie, plotFactor=bar)
