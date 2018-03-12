from flask import render_template,redirect,request,url_for,flash
from . import auth  # 这是为了路由route上都加上auth
from flask_login import login_required
from flask_login import login_user, logout_user
from .forms import LoginForm, RegistrationForm
from ..models import User,db



'''
登录页面
'''
@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)#用户登录
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invaild username or password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user() #退出登录
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

#为了保护路由只让认证用户访问，flask-login提供了 login_required秀时期
@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed'


#注册之后跳转到登录页面，跳转这种只在views层进行逻辑的操作
@auth.route('/register',methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,password=form.password.data)
        db.session.add(user)
        flash('You can login now.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)