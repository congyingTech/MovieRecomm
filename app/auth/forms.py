from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

class LoginForm(Form): #用户登录表单
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remeber_me = BooleanField('Keep me logged in')
    submit = SubmitField('LogIn')

class RegistrationForm(Form):#用户注册表单
    email = StringField('Email',validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators =[DataRequired()])
    username = StringField('UserName', StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')]))
    submit = SubmitField('Register')

    #在表单类中，如果定义了以validate_开头且后面跟着字段名的方法，它就和常规验证函数一起调用
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already registered.')
