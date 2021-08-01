from wtforms.fields.core import SelectMultipleField
from wtforms.fields.simple import HiddenField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    lng = HiddenField("lng")
    lat = HiddenField("lat")
    address = HiddenField('Address', validators=[DataRequired()])
    languages = SelectMultipleField("Languages", choices=[], validators=[DataRequired()])
    submit = SubmitField('Post')

class LangForm(FlaskForm):
    language = StringField('Language')
    submit = SubmitField('Save')