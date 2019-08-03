from flask import Blueprint, render_template
from collections import Counter
from coding_tool.models import Publication
from coding_tool.metadata.util import create_plot

import numpy as np

metadata = Blueprint('metadata', __name__)


@metadata.route("/metadata/authors")
def authors():
    c = Counter()
    publications = Publication.query.all()
    for pub in publications:
        c.update(map(str.strip, pub.authors.split(';')))
    return render_template('most_authors.html', most_common_authors=c.items())


@metadata.route("/metadata/institutions")
def institutions():
    c = Counter()
    publications = Publication.query.all()
    for pub in publications:
        c.update(map(str.strip, pub.institution.split(';')))
    return render_template('institution.html', most_common_institutions=c.items())


@metadata.route("/metadata/years")
def years():
    c = Counter()
    publications = Publication.query.all()
    for pub in publications:
        c.update([pub.year])
    bar = create_plot(c)
    return render_template('plot.html', plot=bar)


@metadata.route("/metadata/venues")
def venues():
    c = Counter()
    publications = Publication.query.all()
    for pub in publications:
        c.update([pub.venue])
    bar = create_plot(c)
    return render_template('plot.html', plot=bar)


@metadata.route("/metadata")
def metadata_main():
    counter_venues = Counter()
    counter_years = Counter()
    counter_institutions = Counter()
    counter_authors = Counter()
    publications = Publication.query.all()
    for pub in publications:
        counter_venues.update([pub.venue])
        counter_years.update([pub.year])
        counter_institutions.update(map(str.strip, pub.institution.split(';')))
        counter_authors.update(map(str.strip, pub.authors.split(';')))

    bar_venues = create_plot(counter_venues)
    bar_years = create_plot(counter_years)
    return render_template('metadata.html', plot_venues=bar_venues, plot_years=bar_years,
                           most_common_authors=counter_authors.most_common(11),
                           most_common_institutions=counter_institutions.most_common(7))
