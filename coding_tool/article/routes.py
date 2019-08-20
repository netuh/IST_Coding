from flask import Blueprint, render_template, url_for, redirect
from collections import Counter


from coding_tool.util import create_plot_pie, create_plot_violin, create_plot_bar
from coding_tool.article.forms import SelectArticleForm
from coding_tool.models import *

import numpy as np

articles = Blueprint('articles', __name__)


@articles.route("/article/select", methods=['GET', 'POST'])
def select_articles():
    form = SelectArticleForm()
    guielines_list = []
    guidelines = Guideline.query.with_entities(Guideline.title).all()
    for a_guideline in guidelines:
        guielines_list.append((a_guideline.title, a_guideline.title))
    form.guidelines.choices = guielines_list
    design_list = []
    for name, member in DesignType.__members__.items():
        design_list.append((member.value, member.value))
    form.designs.choices = design_list
    task_type_list = []
    for name, member in TaskType.__members__.items():
        task_type_list.append((member.value, member.value))
    form.performed_tasks.choices = task_type_list
    nature_of_data_list = []
    for name, member in NatureOfDataSource.__members__.items():
        nature_of_data_list.append((member.value, member.value))
    form.nature_of_data.choices = nature_of_data_list
    DurationType
    duration_list = []
    for name, member in DurationType.__members__.items():
        duration_list.append((member.value, member.value))
    form.duration.choices = duration_list
    profile_list = []
    for name, member in ProfileType.__members__.items():
        profile_list.append((member.value, member.value))
    form.profile_type.choices = profile_list
    if form.validate_on_submit():
        return redirect(url_for('sampling.detail_article', charac_name='test'))
    return render_template('select_articles.html', form=form)


@articles.route("/article/<pub_id>", methods=['GET', 'POST'])
def detail_article():
    return render_template('detail_article.html')
