import os
import pandas as pd
from coding_tool import db
from flask import render_template, request, Blueprint, url_for
from coding_tool.models import Publication

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)

    publications = Publication.query.all()
    return render_template('home.html', publications=publications)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/data")
def data():
    publications = Publication.query.all()
    return render_template('home.html', publications=publications)
