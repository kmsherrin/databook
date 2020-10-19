from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired



class TagForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired()])

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField(u'Post Category', choices=[('General', 'General'), ('Atmospheric', 'Atmospheric'), ('Oceanographic', 'Oceanographic'), ('Geology', 'Geology')])
    
    tags = FieldList(StringField('Tag', [DataRequired()]), max_entries=10)
    
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('Add Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class CommentReplyForm(FlaskForm):
    parent_comment = StringField('Parent Comment')
    content = TextAreaField('Reply', validators=[DataRequired()])

    submit = SubmitField('Post Reply')


