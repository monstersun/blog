from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    summary = TextAreaField('摘要', validators=[DataRequired()])
    body = TextAreaField('正文', validators=[DataRequired()])

