import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
import sqlite3
import re,json,logging
from urllib.parse import urlencode

'''
因为有355页的数据，所以采用多线程爬虫
'''
def main():
    url_list = []
    for i in range(0, 340, 20):
        data = {
            'type': 'movie',
            'tag': '热门',
            'sort': 'recommend',
            'page_limit': 20,
            'page_start': i
        }
        #urlencode是将data以url格式编码
        url = 'https://movie.douban.com/j/search_subjects?' + urlencode(data)
        url_list.append(url)

    logging.info("url_list is %s" % url_list)
    pool = ThreadPool()
    results = pool.map(one_page, url_list)
    pool.close()
    pool.join()
    print('main ended')


'''
保存
'''
def save_data(film):

    title = film['title']
    rate = film['rate']
    url = film['url']
    cover_url = film['cover_url']
    types = film['types']
    actors = film['actors']
    content = film['content']
    create_time = film['create_time']

    logging.info(type(title))
    logging.info(type(rate))
    logging.info(type(url))
    logging.info(type(cover_url))
    logging.info(type(types))
    logging.info(type(actors))
    logging.info(type(content))
    logging.info(type(create_time))





    with sqlite3.connect("data-dev.sqlite") as conn:
        cursor = conn.cursor()
        # 插入数据
        insert_sql = "insert into films(title,rate,url,cover_url,types,actors,content,create_time) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"
        cursor.execute(insert_sql % (title,rate,url,cover_url,types,actors,content,create_time))
        #cursor.execute("insert into films(title,create_time,content,cover_url,download_url) values('title', 'create_time', 'content', 'cover_url', 'download_url')")
        conn.commit()




'''
抓取一个页面的所有电影的url
'''

def one_page(url):
    onePageList = []
    response = requests.get(url, headers=headers)
    html = response.text
    movie = json.loads(html)
    result = []
    if movie and 'subjects' in movie.keys():
        for item in movie.get('subjects'):
            film = {
                    'rate': item.get('rate'), #豆瓣评分
                    'title': item.get('title'), #电影名称
                    'url': item.get('url'), #电影链接
                    'cover_url': item.get('cover'), #电影封面
                    'types':spider_page(item.get('url'))[0], #电影类型
                    'actors': spider_page(item.get('url'))[1], #电影演员
                    'content': spider_page(item.get('url'))[2], #电影内容
                    'create_time': spider_page(item.get('url'))[3] #上映时间
                }
            result.append(film)
            print(film)
            save_data(film)
            logging.info('film has saved in sqlite.')
    print(result)




def spider_page(url):
    response = requests.get(url, headers=headers)
    html = response.text.encode('utf-8')
    tree = etree.HTML(html)

    #电影的内容
    content = re.sub('[\r\n\t]', '', ''.join(tree.xpath('//span[@property="v:summary"]/text()')))

    #电影的类型
    types = ','.join(tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()'))

    #电影的演员
    actors = ','.join(tree.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a[@href]/text()'))

    #上映时间
    create_time = '|'.join(tree.xpath('//span[@property="v:initialReleaseDate"]/text()'))

    return [types,actors,content,create_time]




if __name__ == "__main__":
    # maxPage = 355
    # for i in range(maxPage):
    #     main('http://www.kaixindy.com/category/video/page/%d'%i)
    #
    #
    # title = tree.xpath('//*[@id="content"]/h1/span[1]/text()')
    # content = tree.xpath('//*[@id="link-report"]/span[1]/text()')
    # print(content)
    # url = 'https://movie.douban.com/subject/25790761/'
    # response = requests.get(url, headers=headers)
    # html = response.text.encode('utf-8')
    # tree = etree.HTML(html)
    #
    #
    # print(''.join(tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')))
    # print(tree.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a[@href]/text()'))
    # #content = re.sub('[\r\n\t]', '', ''.join(tree.xpath('//span[@property="v:summary"]/text()')))
    # content = re.sub('[\r\n\t]', '', ''.join(tree.xpath('//span[@property="v:summary"]/text()')))
    #
    # print(content)
    # print(tree.xpath('//span[@property="v:initialReleaseDate"]/text()'))

    main()