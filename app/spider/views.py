from ..models import User
from . import spider
from flask import abort, render_template
import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

#user的movie资料页面
@spider.route('/user/<username>', methods=['GET','POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('favorite.html', user=user)


def spider(url):
    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)
    movie_xpath = tree.xpath('//div[@id="content"]/div/div/a[@href]')
    print(movie_xpath)