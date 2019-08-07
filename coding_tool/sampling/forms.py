from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired

from coding_tool.models import SamplingCharacteristic, Sampling


class SelectingCharacteristicForm(FlaskForm):
    selectedCharac = SelectField('Programming Language')
    submit = SubmitField('Details')
