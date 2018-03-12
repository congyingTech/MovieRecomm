from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128)) #经过散列的密码

    movieContent = db.Column(db.Text()) #这是注册用户下的电影信息


    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self): #@property装饰器就是负责把一个方法变成属性调用的
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #加载用户的回调函数
    from . import login_manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
