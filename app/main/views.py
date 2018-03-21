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
    contents = Film.query.with_entities(Film.content).all()
    for content in contents:
        print(type(content))
        print(list(content))


    #实现分页——渲染的页数从请求的查询字符串(request.args)中获取
    page = request.args.get('page', 1, type=int)
    pagination = Film.query.order_by(Film.create_time.desc()).paginate(
        page, per_page=current_app.config['MOVIE_ITEM_PER_PAGE'], error_out=False
    )
    movie = pagination.items
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow(), movie=movie,
                           pagination =  pagination)

