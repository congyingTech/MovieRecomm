from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, request,current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import Film

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    # #context将数据传入前台
    # context = {
    #     'films':Film.query.all()
    # }
    #contents = Film.query.with_entities(Film.content).all()
    # for content in contents:
    #     print(type(content))
    #     print(list(content))
    title = ''
    allData = Film.query.order_by(Film.title.desc()).all()
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
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow(), films=films,
                           pagination =  pagination)

@main.route('/content/detail/<film_id>', methods=['GET', 'POST'])
def detail(film_id):
    film = Film.query.filter(Film.id==film_id).all()[0]
    actors = film.actors.split(',')
    actorList = []
    lenth = int(len(actors)/3)
    for i in range(lenth-1):
        actorList.append(actors[i::3])

    print(film)
    return render_template('content/detail.html', film=film, actorList=actorList)

@main.route('/search/', methods=['GET', 'POST'])
def search():
    q = request.args.get('q')
    print(q)
    films = Film.query.filter(Film.title==q.format()).all()
    print(films)
    return render_template('index.html', films=films)

@main.route('/favorite', methods=['GET', 'POST'])
def favorite():
    pass


@main.route('/content/ownmovie/<username>', methods=['GET', 'POST'])
def ownmovie(username):
    return render_template('content/ownmovie.html', username=username)
@main.route('/content/recomm/<username>', methods=['GET', 'POST'])
def recomm(username):
    return render_template('content/recomm.html',username=username)