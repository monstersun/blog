from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    summary = TextAreaField('摘要', validators=[DataRequired()])
    body = PageDownField('正文', validators=[DataRequired()])

