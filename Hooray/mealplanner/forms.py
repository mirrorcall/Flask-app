from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('keyword', validators=[DataRequired()])
 
