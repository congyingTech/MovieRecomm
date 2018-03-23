import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import sqlite3
import re,json,logging,random
from urllib.parse import urlencode
from urllib.request import ProxyHandler, build_opener


# proxys = [{"http" : "110.73.50.119:8123"},
#             {"http" : "117.90.1.251:9000"},
#             {"http" : "115.223.231.69:9000"},
#             {"http" : "115.223.215.229:9000"},
#             {"http" : "218.95.51.46:9000"}]

# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9
# Cache-Control: max-age=0
# Connection: keep-alive
# Cookie: gr_user_id=9b25012a-368b-4cae-83f3-64f354dea4e3; __yadk_uid=AbvC7FbybsNL12s1aJWph6pmLcOxjoId; _ga=GA1.2.38940058.1482233398; ll="108288"; ue="bupt_wcy@163.com"; _vwo_uuid_v2=7909A73FF60DCF86621E6F0076C2F484|35bed231f1a504e0015873dc743eeac6; bid=XXpemV2uN_o; push_noty_num=0; push_doumail_num=0; viewed="10594787_1051193_2154960_1011228_26902009_26886337_24703171_2230244_1882382_1274001"; ap=1; __utmv=30149280.13901; ps=y; __utmz=30149280.1521600809.15.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ct=y; __utmc=30149280; __utma=30149280.38940058.1482233398.1521683655.1521689851.21; __utma=223695111.1420860989.1482233398.1521627913.1521689855.67; __utmb=223695111.0.10.1521689855; __utmc=223695111; __utmz=223695111.1521689855.67.48.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/note/185257401/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1521689855%2C%22https%3A%2F%2Fwww.douban.com%2Fnote%2F185257401%2F%22%5D; _pk_ses.100001.4cf6=*; as="https://movie.douban.com/"; __utmt=1; regpop=1; __utmt_douban=1; _pk_id.100001.4cf6=9d8748bcfa17b8a1.1482233399.69.1521690826.1521628245.; __utmb=30149280.12.10.1521689851
# Host: movie.douban.com
# Referer: https://movie.douban.com/
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36


headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
           'Referer': 'https://movie.douban.com/',
           'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
           }





#headers = ("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
# proxy = random.choice(proxys)
# print(proxy)
#urllib使用代理
# proxy_support = ProxyHandler(proxy)
# opener = build_opener(proxy_support)
# opener.addheaders = [headers]


'''
因为有355页的数据，所以采用多线程爬虫
'''
def main():
    url_list = []
    for i in range(0, 340, 20):
        data = {
            'type': 'movie',
            'tag': '经典',
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

    id = film['id']
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
        insert_sql = "insert or ignore into films(id,title,rate,url,cover_url,types,actors,content,create_time) values('%d','%s','%s','%s','%s','%s','%s','%s','%s');"
        sql = insert_sql % (id, title, rate, url, cover_url, types, actors.replace("'", "''"), content.replace("'", "''"), create_time)
        #update_sql = ""
        # select_sql = "select * from films where id=%d" % id
        # print(select_sql)
        # result = cursor.execute(select_sql).fetchone()
        # # if result == None:
        #     sql = insert_sql % (id, title, rate, url, cover_url, types, actors.replace("'", "''"), content.replace("'", "''"), create_time)
        #
        # else:
        #     sql =
        print(sql)
        cursor.execute(sql)
        #cursor.execute("insert into films(title,create_time,content,cover_url,download_url) values('title', 'create_time', 'content', 'cover_url', 'download_url')")
        conn.commit()




'''
抓取一个页面的所有电影的url
'''

def one_page(url):
    onePageList = []
    #
    response = requests.get(url, headers=headers)
    html = response.text
    #r = opener.open(url)
    #html = r.read().decode('utf-8')
    movie = json.loads(html)
    result = []
    if movie and 'subjects' in movie.keys():
        for item in movie.get('subjects'):
            film = {
                    'rate': item.get('rate'), #豆瓣评分
                    'title': item.get('title'), #电影名称
                    'url': item.get('url'), #电影链接
                    'cover_url': item.get('cover'), #电影封面
                    'id': spider_page(item.get('url'))[0], #电影id
                    'types':spider_page(item.get('url'))[1], #电影类型
                    'actors': spider_page(item.get('url'))[2], #电影演员
                    'content': spider_page(item.get('url'))[3], #电影内容
                    'create_time': spider_page(item.get('url'))[4] #上映时间
                }
            result.append(film)
            print(film)
            save_data(film)
            logging.info('film has saved in sqlite.')
    print(result)




def spider_page(url):
    #r = opener.open(url)
    #html = r.read().decode('utf-8')

    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)

    #电影的id
    id = int(re.findall(r'\d+', url)[0])

    #电影的内容
    content = re.sub('[\r\n\t]', '', ''.join(tree.xpath('//span[@property="v:summary"]/text()')))

    #电影的类型
    types = ','.join(tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()'))

    #电影的演员
    actors = ','.join(tree.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a[@href]/text()'))

    #上映时间
    create_time = '|'.join(tree.xpath('//span[@property="v:initialReleaseDate"]/text()'))

    return [id,types,actors,content,create_time]




if __name__ == "__main__":
    main()
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
   #  proxies = {"http": "110.73.50.119:8123",
   #             "http": "117.90.1.251:9000",
   #             "http": "115.223.231.69:9000",
   #             "http": "115.223.215.229:9000",
   #             "http": "218.95.51.46:9000"}

    # url = 'https://movie.douban.com/subject/26977165/'
    # response = requests.get(url, headers=headers)
    # html = response.text.encode('utf-8')
    # tree = etree.HTML(html)
    # # 电影的内容
    # content = re.sub('[\r\n\t]', '', ''.join(tree.xpath('//span[@property="v:summary"]/text()')))
    # print(content)
    # # 电影的类型
    # types = ','.join(tree.xpath('//*[@id="info"]/span[@property="v:genre"]/text()'))
    # print(types)
    # # 电影的演员
    # actors = ','.join(tree.xpath('//*[@id="info"]/span[@class="actor"]/span[@class="attrs"]/a[@href]/text()'))
    # print(actors)
    # # 上映时间
    # create_time = '|'.join(tree.xpath('//span[@property="v:initialReleaseDate"]/text()'))
    #print(create_time)
    # headerss = ("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
    # proxy = random.choice(proxys)
    # url = 'https://movie.douban.com/subject/25790761/'
    #
    # print(proxy)
    # #urllib使用代理
    # proxy_support = ProxyHandler(proxy)
    # opener = build_opener(proxy_support)
    # opener.addheaders = [headerss]
    #
    # r = opener.open(url)
    # html = r.read().decode('utf-8')

    #print(html)
    # ip = ["110.73.50.119:8123","117.90.1.251:9000","115.223.231.69:9000","115.223.215.229:9000"]
    # proxies = {"http":random.choice(ip)}
    # proxy = {'http': '27.24.158.155:84'}
    # print(proxies)
    # url = 'http://ip.chinaz.com/'
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36',
    #     'Connection': 'keep-alive'}
    # response = requests.get(url=url, proxies=proxy, headers=headers)
    # response.encoding = 'utf-8'
    # html = response.text
    # print(html)

