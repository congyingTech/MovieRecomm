from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#表单类
class NameForm(FlaskForm):
    name = StringField('输入你的名字', validators=[DataRequired()])
    submit = SubmitField('提交')