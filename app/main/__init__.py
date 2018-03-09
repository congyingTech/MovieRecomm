#使用蓝本定义路由——蓝本中定义的路由处于休眠，直到蓝本注册到app上，路由成为app的一部分
#main于是成了一个蓝本

from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors  #程序的路由保存在views中，而错误处理程序保存在errors中；导入这俩即可关联蓝本


