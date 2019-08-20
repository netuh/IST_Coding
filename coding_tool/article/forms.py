from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField, BooleanField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, InputRequired, NumberRange
#from wtforms.widgets import CheckboxInput, ListWidget


class SelectArticleForm(FlaskForm):
    sample_size_min = IntegerRangeField(
        'Sample Size Min', [NumberRange(min=1, max=100)], default=1)
    sample_size_max = IntegerRangeField(
        'Sample Size Max', [NumberRange(min=1, max=100)], default=100)
    guidelines = SelectField('Adopted Guidelines')
    designs = SelectField('Desing of Experiments')
    performed_tasks = SelectMultipleField('Task Types')
    profile_type = SelectMultipleField('Profiles')
    nature_of_data = SelectMultipleField(
        'Nature of Data Source')
    duration = SelectField('Duration')
    lab_settings = BooleanField(
        'Performed in a Lab', validators=[DataRequired()])
    list_all = SubmitField('List All')
