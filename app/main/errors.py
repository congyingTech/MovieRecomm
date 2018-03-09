from flask import render_template
from . import main


#app_errorhandler只有蓝本main中的错误才能触发
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(505)
def internal_server_error(e):
    return render_template('500.html'),500

