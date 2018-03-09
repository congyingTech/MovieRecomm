from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import  Required

#表单类
class NameForm(Form):
    name = StringField('输入你的名字', validators=[Required()])
    submit = SubmitField('提交')