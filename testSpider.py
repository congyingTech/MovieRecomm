import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}


'''
抓取一个页面的所有电影的url
'''
def main(url):
    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)
    movie_urls = tree.xpath('//div[@id="content"]/div/div/a[@href]/@href')
    print(movie_urls)
    for url in movie_urls:
        spider(url)


def spider(url):
    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)

    title = tree.xpath('//div[@id="content"]/div/h2/text()');new_title = []
    for i in title:
        new_title.append(i.strip().split('》')[0][1:])
    title = new_title
    content = tree.xpath('//div[@id="content"]/div/div/p/text()')
    for item in enumerate(content):
        if len(item) == 0:
            item = tree.xpath('//div[@id="content"]/div/div/div/p/text()')
    print(content)
    createTime = tree.xpath('//div[@id="content"]/div/div/span[@class="post-info-date"]/a/text()')





if __name__ == "__main__":
    # maxPage = 355
    # for i in range(maxPage):
    #     main('http://www.kaixindy.com/category/video/page/%d'%i)
    main('http://www.kaixindy.com/category/video/')