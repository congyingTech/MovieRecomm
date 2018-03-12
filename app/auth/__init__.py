#auth 蓝图中 里面保存与认证相关的路由
from flask import Blueprint
auth = Blueprint('auth', __name__)
from . import views
