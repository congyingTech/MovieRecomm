import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

def spider(url):
    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)
    movie_xpath = tree.xpath('//div[@id="content"]/div/div/a[@href]/@href')
    title = tree.xpath('//div[@id="content"]/div/h2/a/@title')
    content = tree.xpath('//div[@id="content"]/div/div/p/text()')
    createTime = tree.xpath('//div[@id="content"]/div/div/span[@class="post-info-date"]/a/text()')
    print(title)
    print(movie_xpath)
    print(content)
    print(createTime)




if __name__ == "__main__":
    spider('http://www.kaixindy.com/category/video')