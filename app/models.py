from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from sqlalchemy.exc import IntegrityError
import sqlite3
# ALL_CHOICES = [('romance', '爱情片'), ('drama', '剧情片'), ('comedy', '喜剧片'),('family','家庭片'),
#                    ('ethics', '伦理片'),('literature', '文艺片'),('music','音乐片'),('singing','歌舞片'),
#                    ('action','动作片'),('horror','恐怖片'), ('thriller','惊悚片'),('adventure','冒险片'),
#                    ('war','战争片'),('history','历史片'),('fantasy','科幻片')]
ALL_CHOICES = ['古装', '黑色电影', '悬疑', '动画', '科幻', '家庭', '惊悚', '情色', '音乐', '武侠', '运动', '灾难', '历史', \
               '冒险', '战争', '歌舞', '恐怖', '传记', '犯罪', '爱情', '剧情', '西部', '同性', '动作', '奇幻', '喜剧', '儿童']
DEFAULT_CHOICES = ['爱情', '动作', '科幻']

user_film = db.Table('user_film',
            db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
            db.Column('film_id', db.Integer, db.ForeignKey('films.id'))
                     )

#所有爬取Film的数据库表
class Film(db.Model):
    __tablename__ = 'films'
    #title,rate,url,cover_url,types,actors,content,create_time
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text,  nullable=False)
    rate = db.Column(db.String, nullable=False)
    url = db.Column(db.String,  nullable=False)
    cover_url = db.Column(db.String, nullable=False)
    types = db.Column(db.String,  nullable=False)
    actors = db.Column(db.String,  nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.String,  nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128)) #经过散列的密码
    moviePrefer = db.Column(db.Text(64)) #这是注册用户时需要添加的电影偏好标签
    favorite = db.relationship('Film',secondary=user_film,
                                    backref=db.backref('users', lazy='dynamic'),
                                    lazy='dynamic')   #这是注册用户喜欢的电影id
    #生成user的虚拟数据
    @staticmethod
    def generate_fake_user(count=10):
        from sqlalchemy.exc import IntegrityError
        #from random import seed
        import forgery_py
        maxPreferNum = 6 #maxFavoriteNum = 840
        #seed() 会把随机数固定下来
        for i in range(count):
            import random
            preferNum = random.choice(range(1, maxPreferNum + 1))
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password='password',
                     moviePrefer=str(random.sample(ALL_CHOICES, preferNum))
                )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    #生成favorite的虚拟数据
    @staticmethod
    def generate_fake_favorite():
        maxFavoriteNum = 840;
        user_count = User.query.count()
        import random
        with sqlite3.connect("data-dev.sqlite") as conn:
            cursor = conn.cursor()
            insert_sql = "insert  into user_film(user_id,film_id) values('%d','%d');"
            for i in range(1, user_count + 1):
                favoriteNum = random.choice(range(1, maxFavoriteNum + 1))
                favorite = random.sample(User.get_allFilmId(), favoriteNum)
                for j in favorite:
                    ids = j[0]
                    sql = insert_sql % (i, ids)
                    cursor.execute(sql)
                    conn.commit()

    @staticmethod
    def get_allFilmId():
        all_films = Film.query.with_entities(Film.id).all()
        return all_films

    @staticmethod
    def test():

        return User.query.all()

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




    # @staticmethod
    # def getAllFilms():
    #     all_films = Film.query.with_entities(Film.id).all()
    #     return all_films



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

