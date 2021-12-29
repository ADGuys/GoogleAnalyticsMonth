import time

import requests
from lxml import etree
import pymysql
import pymongo
import random


def get_proxy():

    return pool


def mysql_db(item):
    connect = pymysql.connect(host='23.92.27.129', user='root', passwd='loctek', db='10why', charset='utf8')
    cursor = connect.cursor()
    sqls = '''select * from douban_book where url = %s'''
    va = item['url']
    cursor.execute(sqls, va)
    results1 = cursor.fetchall()
    results = len(results1)
    if results == 0:
        cursor.execute(
            """insert into douban_book(url, type) value ("{}", "{}")""".format(
                item['url'], item['type']
            )
        )
        # 执行sql
        print('插入')
        connect.commit()


def delete_proxy(self, proxy):
    if proxy:
        self.pool.pop(self.index)


def get_proxy_url(ip_port):
    index = random.randint(0, len(ip_port) - 1)
    proxy = {"https": "https://" + ip_port[index]}
    return proxy


arr_new = []
proxy_list = get_proxy()  # get proxy
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
}
print(proxy_list)
url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
response = requests.get(url, headers=headers, proxies=get_proxy_url(proxy_list))
html = etree.HTML(response.text)
arr = html.xpath('//table[@class="tagCol"]//td/a/text()')

for item in arr:
    proxy_list = get_proxy()
    url_item = 'https://book.douban.com/tag/' + item
    response_item = requests.get(url_item, headers=headers, proxies=get_proxy_url(proxy_list))
    response_item_html = etree.HTML(response_item.text)
    next_url_page = response_item_html.xpath('//span[@class="next"]/a/@href')
    index = 1
    while index <= 50 and next_url_page:
        proxy_list = get_proxy()
        next_url = 'https://book.douban.com/' + next_url_page[0]
        index += 1
        response_item_index = response_item = requests.get(next_url, headers=headers,
                                                           proxies=get_proxy_url(proxy_list))
        response_item_index_html = etree.HTML(response_item_index.text)
        information_urls = response_item_index_html.xpath('//h2/a/@href')
        next_url_page = response_item_index_html.xpath('//span[@class="next"]/a/@href')
        if information_urls:
            for url_page in information_urls:
                total_item = {
                    'type': item,
                    'url': url_page
                }
                mysql_db(total_item)
