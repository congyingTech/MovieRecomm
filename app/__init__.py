from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong' #none,basic,strong
login_manager.login_view = 'auth.login'#设置登录页面的端点


'''
创建app的工厂函数createApp
'''
def createApp(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    #注册蓝本main——这样main中的路由和错误处理程序便注册到了app上
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #注册蓝本auth——这样认证的路由都注册到了app上
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
