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
    profiles = SamplingProfile.query.all()
    word_list = []
    c = Counter()
    for a_profile in profiles:
        word_list.append(a_profile.profile.strip().lower())
    c.update(word_list)
    pie = create_plot_pie(c)
    return render_template('distribution.html', plot=pie)


@sampling.route("/sampling/violin")
def sampling_violin():
    profiles = SamplingProfile.query.all()
    total_data = []
    professional_data = []
    student_data = []
    for a_profile in profiles:
        total_data.append(int(a_profile.quantity))
        if (a_profile.profile == 'professional'):
            professional_data.append(int(a_profile.quantity))
        else:
            student_data.append(int(a_profile.quantity))
    violin = create_plot_violin(
        total=total_data, professionals=professional_data, students=student_data)
    return render_template('violin.html', plot=violin)
