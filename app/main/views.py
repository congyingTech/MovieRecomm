from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, request,current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import Film, User
from flask_login import  current_user

@main.route('/', methods=['GET', 'POST'])
def index():
    # form = NameForm()
    # name = form.name.data
    # print(name)
    # if form.validate_on_submit():
    #
    #
    #     form.name.data = ''
    #     return redirect(url_for('.index'))
    # #context将数据传入前台
    # context = {
    #     'films':Film.query.all()
    # }

    #contents = Film.query.with_entities(Film.content).all()
    # for content in contents:
    #     print(type(content))
    #     print(list(content))
    # first_data = Film.query.first()
    # for film in allData:
    #     if film.title == '' or film.create_time =='' or film.actors =='' or film.cover_url =='' or film.url =='' or \
    #         film.content =='' or film.rate =='' or film.types =='' or film.title==title:
    #         title = film.title
    #         db.session.delete(film)
    #     title = film.title
    # db.session.add(first_data)
    #实现分页——渲染的页数从请求的查询字符串(request.args)中获取
    page = request.args.get('page', 1, type=int)
    movie_data = Film.query.order_by(Film.create_time.desc(), Film.rate.desc())
    #movie_title = db.session.query(Film.title).distinct().all()
        #movie = Film.query.filter_by(title==title).order_by(Film.create_time.desc()).first()
    pagination = movie_data.paginate(
        page, per_page=current_app.config['MOVIE_ITEM_PER_PAGE'], error_out=False
    )
    films = pagination.items

    all_films = Film.query.all()

    favorites = []
    if current_user.is_authenticated:
        email = current_user.email
        user = User.query.filter(User.email == email).first()
        favorites = user.favorite.all()
    return render_template('index.html', name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow(), films=films,
                           pagination =  pagination, favorites=favorites)

@main.route('/content/detail/<film_id>', methods=['GET', 'POST'])
def detail(film_id):
    film = Film.query.filter(Film.id==film_id).all()[0]
    actors = film.actors.split(',')
    actorList = []
    lenth = int(len(actors)/3)
    for i in range(lenth-1):
        actorList.append(actors[i::3])

    return render_template('content/detail.html', film=film, actorList=actorList)

@main.route('/search/', methods=['GET', 'POST'])
def search():
    q = request.args.get('q')
    films = Film.query.filter(Film.title==q.format()).all()
    return render_template('index.html', films=films)

#将film添加到favorite列表
@main.route('/favorite/<film_id>', methods=['GET', 'POST'])
def favorite(film_id):
    email = current_user.email
    user = User.query.filter(User.email == email).first()
    user.favorite.append(Film.query.get(film_id))

    return redirect(url_for('main.index'))
#将film从favorite列表移除
@main.route('/unfavorite/<film_id>', methods=['GET', 'POST'])
def unfavorite(film_id):
    email = current_user.email
    user = User.query.filter(User.email == email).first()
    user.favorite.remove(Film.query.get(film_id))

    return redirect(url_for('main.index'))


#favorite的全部电影的展示页面favorite.html
@main.route('/content/favorite/<username>', methods=['GET', 'POST'])
def favoriteAll(username):
    if current_user.is_authenticated:
        email = current_user.email
        user = User.query.filter(User.email == email).first()
        favorites = user.favorite.all()


    return render_template('content/favorite.html', username=username, favorites=favorites)
#将favorite从favorite.html移除
@main.route('/remove/<film_id>')
def remove(film_id):
    email = current_user.email
    user = User.query.filter(User.email == email).first()
    user.favorite.remove(Film.query.get(film_id))

    return redirect(url_for('main.favoriteAll', username=current_user.username))

@main.route('/content/recomm/<username>', methods=['GET', 'POST'])
def recomm(username):
    return render_template('content/recomm.html',username=username)


def getAllTypes():
    all_types = Film.query.with_entities(Film.types).all()
    type_list = []
    type_list1 = []
    for i, film in enumerate(all_types):
        type_list.extend(list(film))
        type_list1.extend(i for i in type_list[i].split(',') if i != '')
    type_list = list(set(type_list1))
    return type_list

def getAllFilms():
    all_films = Film.query.all()
    return all_films