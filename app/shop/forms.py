from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired(),])
    description = StringField('Post Content', validators=[DataRequired(),])
    submit = SubmitField()