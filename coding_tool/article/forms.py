from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField, BooleanField, IntegerField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.widgets import html5
from wtforms.validators import NumberRange


class SelectArticleForm(FlaskForm):
    max_value = 196
    min_value = 2
    sample_size_min = IntegerField(
        'Telephone', [NumberRange(min=2, max=196)], widget=html5.NumberInput(), default=2)
    sample_size_max = IntegerField(
        'Telephone', [NumberRange(min=2, max=196)], default=196)
    designs = SelectField('Desing of Experiments')
    performed_tasks = SelectMultipleField('Task Types')
    recruting_type = SelectMultipleField('Recruitments')
    profile_type = SelectMultipleField('Profiles')
    nature_of_data = SelectMultipleField(
        'Nature of Data Source')
    duration = SelectField('Duration')
    lab_settings = BooleanField(
        'Performed in a Lab')
    list_all = SubmitField('List All')
