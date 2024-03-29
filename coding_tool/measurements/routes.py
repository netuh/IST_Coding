from flask import Blueprint, render_template
from coding_tool.models import Measurement, NatureOfDataSource
from coding_tool.util import create_plot_pie, create_plot_violin, create_plot_bar

from collections import Counter
import numpy as np

measurements = Blueprint('measurements', __name__)


@measurements.route("/measurements/general/")
def all():
    measurements = Measurement.query.all()
    c = Counter()
    for m in measurements:
        c.update([m.measurement_type.value])
    pie = create_plot_bar(c)
    return render_template('measurements_general.html', plot=pie)


@measurements.route("/measurements/subjective/")
def subjectives():
    m_list = Measurement.query.filter_by(
        measurement_type=NatureOfDataSource.SUBJECTIVE)
    c = Counter()
    for m in m_list.all():
        if m.measurement_instruments:
            c.update(m.measurement_instruments.replace(" ", "").split(';'))
    bar = create_plot_bar(c)
    return render_template('subjective_measurements.html', plot=bar)


@measurements.route("/measurements/source_code/")
def objectives():
    m_list = Measurement.query.filter_by(
        measurement_type=NatureOfDataSource.SOURCE_CODE)
    c = Counter()
    for m in m_list.all():
        if m.measurement_instruments:
            c.update(m.measurement_instruments.replace(" ", "").split(';'))
    bar = create_plot_bar(c)
    return render_template('objective_measurements.html', plot=bar)


@measurements.route("/measurements/time/")
def time():
    m_list = Measurement.query.filter_by(
        measurement_type=NatureOfDataSource.TIME)
    c = Counter()
    for m in m_list.all():
        if m.measurement_instruments:
            c.update(m.measurement_instruments.replace(" ", "").split(';'))
    bar = create_plot_bar(c)
    return render_template('objective_measurements.html', plot=bar)
