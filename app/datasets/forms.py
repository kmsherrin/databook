from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, FieldList
from wtforms.validators import DataRequired

class DatasetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    abstract = TextAreaField('Dataset Abstract', validators=[DataRequired()])
    
    category = SelectField(u'Dataset Category', choices=[('General', 'General'), ('Atmospheric', 'Atmospheric'), ('Oceanographic', 'Oceanographic'), ('Geology', 'Geology')])
    
    #tags = FieldList(StringField('Tag', [DataRequired()]), max_entries=10)
    datasets = FileField(label='Update Dataset', validators=[FileAllowed(['csv', 'nc', 'ts', '']), FileRequired()])

    submit = SubmitField('Post')


class TagForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired()])

