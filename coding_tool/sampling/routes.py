from flask import Blueprint, render_template
from collections import Counter

from coding_tool.models import Publication, Sampling, SamplingProfile
from coding_tool.sampling.util import create_plot_pie, create_plot_violin


import numpy as np

sampling = Blueprint('sampling', __name__)


@sampling.route("/samplings")
def all_sampling():
    samplings = Sampling.query.all()
    return render_template('samplings.html', samplings=samplings)


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


@sampling.route("/sampling/by_characteristics")
def sampling_characteristics():
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
