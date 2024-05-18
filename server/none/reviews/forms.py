from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class ExpirenceForm(FlaskForm):
    rating = IntegerField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('post')

class ReviewForm(FlaskForm):
    rating = IntegerField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('post')
