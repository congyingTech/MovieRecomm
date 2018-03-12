from ..models import User
from . import content
from flask import abort, render_template
#user的movie资料页面
@content.route('/user/<username>', methods=['GET','POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)