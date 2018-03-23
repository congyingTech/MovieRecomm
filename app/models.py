from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128)) #经过散列的密码
    moviePrefer = db.Column(db.Text(64)) #这是注册用户时需要添加的电影偏好标签

    #movieContent = db.Column(db.Text()) #这是注册用户下的电影信息


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


#所有爬取Film的数据库表
class Film(db.Model):
    __tablename__ = 'films'
    #title,rate,url,cover_url,types,actors,content,create_time
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    rate = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    cover_url = db.Column(db.String, unique=True ,nullable=False)
    types = db.Column(db.String, unique=True, nullable=False)
    actors = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.Text, unique=True, nullable=False)
    create_time = db.Column(db.String, unique=True, nullable=False)



#用户信息数据库表
class UserMovie(db.Model):
    __tablename__ = 'usermovies'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            print('post does not have a body')
        return UserMovie(body=body)

