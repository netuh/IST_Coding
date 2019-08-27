from flask import Blueprint, render_template, url_for, redirect, request
from collections import Counter

import json

from coding_tool.util import create_plot_pie, create_plot_violin, create_plot_bar
from coding_tool.article.forms import SelectArticleForm
from coding_tool.models import *
from coding_tool import db

import numpy as np

articles = Blueprint('articles', __name__)


@articles.route("/articles/select", methods=['GET', 'POST'])
def select_articles():
    form = SelectArticleForm()
    qry = db.session.query(db.func.max(SamplingProfile.quantity).label("max_score"),
                           db.func.min(SamplingProfile.quantity).label(
                               "min_score"),
                           )
    res = qry.one()
    form.max_value = res.max_score
    form.min_value = res.min_score

    guielines_list = []
    guidelines = Guideline.query.with_entities(Guideline.title).all()
    for a_guideline in guidelines:
        guielines_list.append((a_guideline.title, a_guideline.title))
    form.guidelines.choices = guielines_list
    design_list = [('-None-', '-None-')]
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
    duration_list = [('-None-', '-None-')]
    for name, member in DurationType.__members__.items():
        duration_list.append((member.value, member.value))
    form.duration.choices = duration_list
    profile_list = []
    for name, member in ProfileType.__members__.items():
        profile_list.append((member.value, member.value))
    form.profile_type.choices = profile_list

    recruitment_list = []
    for name, member in RecrutingType.__members__.items():
        recruitment_list.append((member.value, member.value))
    form.recruting_type.choices = recruitment_list
    if form.validate_on_submit():
        print('here1')
        data = {}
        data['min'] = form.sample_size_min.data
        data['max'] = form.sample_size_max.data
        if form.guidelines.data:
            data['guideines'] = form.guidelines.data
        if form.nature_of_data.data:
            data['nature_of_data'] = form.nature_of_data.data
        if form.performed_tasks.data:
            data['performed_tasks'] = form.performed_tasks.data
        if form.profile_type.data:
            data['profile_type'] = form.profile_type.data

        if form.designs.data != '-None-':
            data['design'] = form.designs.data
        if form.duration.data != '-None-':
            data['duration'] = form.duration.data
        messages = json.dumps(data)
        print('here3')
        return redirect(url_for('articles.list_articles', page=1, messages=messages))
    print('here4')
    return render_template('select_articles.html', form=form)


@articles.route("/articles/list", methods=['GET', 'POST'])
def list_articles():
    page = request.args.get('page', 1, type=int)
    messages = request.args['messages']
    p = json.loads(messages)

    min_s = int(p['min'])
    max_s = int(p['max'])
    query_result = db.session.query(
        Publication
    ).join(
        Experiment
    ).join(
        Sampling
    ).join(
        ExperimentDesign
    )

    # query_result = db.session.query(
    #     Publication
    # ).join(
    #     Experiment
    # ).join(
    #     Sampling
    # )
    # if 'profile_type' in p:
    #     print('here 1')
    #     query_result.join(SamplingProfile)

    if 'min' in p:
        min_s = int(p['min'])
        print(f'min={min_s}')
        query_result = query_result.filter(
            Sampling.sample_total >= min_s
        )
    if 'max' in p:
        max_s = int(p['max'])
        print(f'max={max_s}')
        query_result = query_result.filter(
            Sampling.sample_total <= max_s
        )
    if 'design' in p:
        var = DesignType(p['design'])
        print(f'design={var}')
        query_result = query_result.filter(
            ExperimentDesign.design == var
        )
    # if 'profile_type' in p:
    #     for a_profile in p['profile_type']:
    #         query_result = query_result.filter(
    #             SamplingProfile.profile == ProfileType(a_profile)
    #         )
    print(f'count={query_result.count()}')
    articles = query_result.paginate(page=page, per_page=10)
    return render_template('detail_article.html', posts=articles, messages=messages)
