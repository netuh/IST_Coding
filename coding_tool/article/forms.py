from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired

from coding_tool.models import SamplingCharacteristic, Sampling


class SelectArticleForm(FlaskForm):
    sample_size = IntegerField('Sample Size')
    guidelines = SelectMultipleField('Adopted Guidelines', choices=[(
        'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    designs = SelectField('Desing of Experiments', choices=[
                          ('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    performed_tasks = SelectMultipleField('Task Types', choices=[(
        'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    measuriments = SelectMultipleField('Measuriment types', choices=[(
        'cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    list_all = SubmitField('List All')
