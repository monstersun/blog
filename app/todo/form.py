from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import Required
from ..model import Category

class ListForm(FlaskForm):
    event = TextAreaField('今日目标', validators=[Required()])
    category = SelectField('类别',coerce=int)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]