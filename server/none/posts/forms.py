from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from app.models import City, Category

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    city = SelectField('City', choices=[(city.value) for city in City], validators=[DataRequired()])
    picture = FileField('Instrument Picture', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', choices=[(category.value) for category in Category], validators=[DataRequired()])
    submit = SubmitField('post')
