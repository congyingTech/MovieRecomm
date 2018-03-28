from random import *
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, user_film, Film

ALL_CHOICES = ['古装', '黑色电影', '悬疑', '动画', '科幻', '家庭', '惊悚', '情色', '音乐', '武侠', '运动', '灾难', '历史', \
               '冒险', '战争', '歌舞', '恐怖', '传记', '犯罪', '爱情', '剧情', '西部', '同性', '动作', '奇幻', '喜剧', '儿童']

DEFAULT_CHOICES = ['爱情', '动作', '科幻']

def users(count=100):
    fake = Faker()
    i = 0
    maxPreferNum = 6; preferNum= random.choice(range(1, maxPreferNum+1))

    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 moviePrefer=str(random.sample(ALL_CHOICES, preferNum)),
                 )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def user_films():
    maxFavoriteNum = 840;
    user_count = User.query.count()
    for i in range(1, user_count+1):
        favoriteNum = random.choice(range(1, maxFavoriteNum + 1))
        favorite = random.sample(get_allFilmId(), favoriteNum)
        for j in favorite:
            uf = user_film(user_id = i,
                           film_id = j
                       )
            db.session.add(uf)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()



def get_allFilmId():
    all_films = Film.query.with_entities(Film.id).all()
    return all_films

# def posts(count=100):
#     fake = Faker()
#     user_count = User.query.count()
#     for i in range(count):
#         u = User.query.offset(randint(0, user_count - 1)).first()
#         p = Post(body=fake.text(),
#                  timestamp=fake.past_date(),
#                  author=u)
#         db.session.add(p)
#     db.session.commit()