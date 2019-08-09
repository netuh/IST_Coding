from flask import Blueprint, render_template, url_for, redirect
from collections import Counter

from coding_tool.models import Publication, Sampling, SamplingProfile
from coding_tool.sampling.util import create_plot_pie, create_plot_violin, create_plot_bar
from coding_tool.sampling.forms import SelectingCharacteristicForm


import numpy as np

sampling = Blueprint('sampling', __name__)


@sampling.route("/sampling/distribution")
def sampling_distribution():
    profiles = Sampling.query.all()
    word_list = []
    c = Counter()
    for a_profile in profiles:
        classification, quantity = a_profile.sample_classification()
        word_list.append(classification)
    c.update(word_list)
    pie = create_plot_pie(c)
    return render_template('distribution.html', plot=pie)


@sampling.route("/sampling/by_classification")
def sampling_classification():
    profiles = Sampling.query.all()
    dic_classification = {}
    dic_classification['total'] = []
    dic_classification['mix'] = []
    dic_classification['professional_only'] = []
    dic_classification['student_only'] = []
    for a_profile in profiles:
        classification, quantity = a_profile.sample_classification()
        dic_classification[classification].append(quantity)
        dic_classification['total'].append(quantity)
    violin = create_plot_violin(dic_classification)
    return render_template('by_classification.html', plot=violin)


@sampling.route("/sampling/by_characteristics", methods=['GET', 'POST'])
def sampling_characteristics():
    this_choices = []
    form = SelectingCharacteristicForm()

    profiles = Sampling.query.all()
    c = Counter()
    for a_profile in profiles:
        for a_charac in a_profile.characteristics:
            c.update([a_charac.charac])
    for a_key in c.keys():
        this_choices.append((a_key, a_key))
    form.selectedCharac.choices = this_choices

    bar = create_plot_bar(c.most_common())

    if form.validate_on_submit():
        return redirect(url_for('sampling.details_charac', charac_name='test'))
    return render_template('by_characteristics.html', plot=bar, title='Login', form=form)


@sampling.route("/sampling/characteristic/<charac_name>/")
def details_charac(charac_name):
    samplings = Sampling.query.all()
    return render_template('samplings.html', samplings=samplings)
