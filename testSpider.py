import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
import sqlite3
import re
'''
因为有355页的数据，所以采用多线程爬虫
'''
def main():
    base_url = 'http://www.kaixindy.com/category/video/page/'
    url_lists = [base_url+str(i) for i in range(1)]
    pool = ThreadPool()
    results = pool.map(one_page, url_lists)
    pool.close()
    pool.join()
    print('main ended')


'''
保存
'''
def save_data(movie):
    title = movie['title']
    create_time = movie['create_time']
    content = movie['content']
    cover_url = movie['cover_url']
    download_url = movie['download_url']
    with sqlite3.connect("data-dev.sqlite") as conn:
        cursor = conn.cursor()
        # 插入数据
        insert_sql = "insert into films(title,create_time,content,cover_url,download_url) values('%s','%s','%s','%s','%s')"
        cursor.execute(insert_sql % (title, create_time, content, cover_url, download_url))
        #cursor.execute("insert into films(title,create_time,content,cover_url,download_url) values('title', 'create_time', 'content', 'cover_url', 'download_url')")
        conn.commit()




'''
抓取一个页面的所有电影的url
'''
def one_page(url):
    onePageList = []
    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)
    movie_urls = tree.xpath('//div[@id="content"]/div/div/a[@href]/@href')
    for url in movie_urls:
        onePageList.append(spider_page(url))
    #print(onePageList)
    return onePageList

def spider_page(url):
    movie = {}
    response = requests.get(url, headers=headers)
    html = response.text
    tree = etree.HTML(html)

    #电影名字
    title = tree.xpath('//div[@id="content"]/div/h2/text()');new_title = []
    for i in title:
        new_title.append(i.strip().split('》')[0][1:])
    title = new_title

    #电影的内容
    content = tree.xpath('//div[@id="content"]/div/div/p/text()')

    #豆瓣评分
    rank = tree.xpath('//div[@id="content"]/div/div/p[starts-with(text(),"豆瓣评分")]')
    print(rank)
    #创建时间
    create_time = tree.xpath('//span[@class="post-info-date"]/text()')

    #下载链接
    download_url = tree.xpath('//div[@id="content"]/div/div[@class="entry"]/a[@href]/@href')
    #电影海报
    cover_url = tree.xpath('//p/img/@src')
    #if (len(title) ==1 and len(content) ==1 and len(create_time) ==1 and len(download_url) ==1 and len(cover_url) ==1):
    if len(title)>0:
        movie['title'] = title[0]
    else:
        movie['title'] = 'Nan'
    if len(content)>0:
        movie['content'] = re.sub('[\r\n\t◎]', '|', ''.join(content))
        print(movie['content'])
    else:
        movie['content'] = 'Nan'
    if len(create_time)>0:
        movie['create_time'] = create_time[0].strip()
    else:
        movie['create_time'] = 'Nan'
    if len(download_url) > 0:
        movie['download_url'] = download_url[0]
    else:
        movie['download_url'] = 'Nan'

    if len(cover_url)>0:
        movie['cover_url'] = cover_url[0]
    else:
        movie['cover_url'] = 'Nan'

    #save_data(movie)

    return movie




if __name__ == "__main__":
    # maxPage = 355
    # for i in range(maxPage):
    #     main('http://www.kaixindy.com/category/video/page/%d'%i)
    main()