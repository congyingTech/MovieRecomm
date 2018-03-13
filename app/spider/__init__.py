from flask import Blueprint
spider = Blueprint('spider', __name__)
from . import views