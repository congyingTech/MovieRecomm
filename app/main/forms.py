from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#表单类
class NameForm(FlaskForm):
    name = StringField('Please input your name', validators=[DataRequired()])

    submit = SubmitField('Submit')
