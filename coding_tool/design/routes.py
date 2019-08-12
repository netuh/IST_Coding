from flask import Blueprint, render_template
from coding_tool.models import ExperimentDesign, Task, Duration
from coding_tool.util import create_plot_pie, create_plot_bar

from collections import Counter

exp_design = Blueprint('exp_design', __name__)


@exp_design.route("/design")
def design():
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
    return render_template('design.html', plotDesign=pie, plotFactor=bar)


@exp_design.route("/design/tasks")
def tasks():
    tasks = Task.query.all()
    count_task_by_type = Counter()
    count_task_by_quantity = Counter()
    for a_task in tasks:
        count_task_by_quantity.update(
            {a_task.task_type.strip().lower(): a_task.quantity})
        count_task_by_type.update([a_task.task_type.strip().lower()])
    plot_by_type = create_plot_bar(count_task_by_type)
    plot_by_quantity = create_plot_bar(count_task_by_quantity)
    return render_template('tasks.html', plot_1=plot_by_type, plot_2=plot_by_quantity)


@exp_design.route("/design/task_duration")
def duration():
    short_duration = Duration.query.filter_by(durantion_type='short')
    long_duration = Duration.query.filter_by(durantion_type='long')
    count_short = Counter()
    for d in short_duration:
        count_short.update([d.classification()])
    count_long = Counter()
    for d in long_duration:
        count_long.update([d.classification()])
    print(count_short)
    print(count_long)
    plot_short = create_plot_pie(count_short)
    plot_long = create_plot_pie(count_long)
    return render_template('duration.html', plot_1=plot_short, plot_2=plot_long)
