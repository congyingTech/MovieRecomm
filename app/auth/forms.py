from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectMultipleField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User

# ALL_CHOICES = [('romance', '爱情片'), ('drama', '剧情片'), ('comedy', '喜剧片'),('family','家庭片'),
#                    ('ethics', '伦理片'),('literature', '文艺片'),('music','音乐片'),('singing','歌舞片'),
#                    ('action','动作片'),('horror','恐怖片'), ('thriller','惊悚片'),('adventure','冒险片'),
#                    ('war','战争片'),('history','历史片'),('fantasy','科幻片')]
# DEFAULT_CHOICES = ['romance', 'action', 'literature']

ALL_CHOICES = [('古装','古装'), ('黑色电影','黑色电影'), ('悬疑','悬疑'), ('动画','动画'), ('科幻','科幻'), ('家庭','家庭'),
               ('惊悚','惊悚'), ('情色','情色'), ('音乐','音乐'), ('武侠','武侠'), ('运动','运动'), ('灾难','灾难'), ('历史','历史'), \
               ('冒险','冒险'), ('战争','战争'), ('歌舞','歌舞'), ('恐怖','恐怖'), ('传记','传记'), ('犯罪','犯罪'), ('爱情','爱情'),\
               ('剧情','剧情'), ('西部','西部'), ('同性','同性'), ('动作','动作'), ('奇幻','奇幻'), ('喜剧','喜剧'), ('儿童','儿童')]

DEFAULT_CHOICES = ['爱情', '动作', '科幻']


class LoginForm(FlaskForm): #用户登录表单
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remeber_me = BooleanField('Keep me logged in')
    submit = SubmitField('LogIn')

class RegistrationForm(FlaskForm):#用户注册表单
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('UserName', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators =[DataRequired()])
    #爱情片、剧情片、喜剧片、家庭片、伦理片、文艺片、音乐片、歌舞片、动漫片、西部片、武侠片、古装片、动作片、恐怖片、惊悚片、冒险片、犯罪片、悬疑片、记录片、战争片、历史片、传记片、体育片、科幻片、魔幻片、奇幻片
    #Romance, drama, comedy, family, ethics, literature and art films, music, singing,  action movies, horror, thriller, adventure,  history, biopic, sports, science fiction and fantasy, fantasy
    moviePrefer = SelectMultipleField('Which type movie you like?', choices = ALL_CHOICES, default=DEFAULT_CHOICES)
    submit = SubmitField('Register')


    #在表单类中，如果定义了以validate_开头且后面跟着字段名的方法，它就和常规验证函数一起调用
    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already registered.')
