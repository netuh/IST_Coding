from flask import Blueprint, render_template, url_for, redirect
from collections import Counter


from coding_tool.util import create_plot_pie, create_plot_violin, create_plot_bar
from coding_tool.article.forms import SelectArticleForm


import numpy as np

articles = Blueprint('articles', __name__)


@articles.route("/article/select", methods=['GET', 'POST'])
def select_articles():
    form = SelectArticleForm()
    if form.validate_on_submit():
        return redirect(url_for('sampling.detail_article', charac_name='test'))
    return render_template('select_articles.html', form=form)


@articles.route("/article/<pub_id>", methods=['GET', 'POST'])
def detail_article():
    return render_template('detail_article.html')
