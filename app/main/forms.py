from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Length, Email

class SearchForm(FlaskForm):
    search_term = StringField('Search', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('🔍')
