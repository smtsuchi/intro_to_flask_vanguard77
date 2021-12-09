from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired(),])
    content = StringField('Post Content', validators=[DataRequired(),])
    submit = SubmitField()