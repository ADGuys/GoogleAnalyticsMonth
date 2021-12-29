import time

import requests
from lxml import etree
import pymysql
import random
import json



def mysql_db(item):
    connect = pymysql.connect(host='east2-vm-database.mysql.database.chinacloudapi.cn', user='loctek@east2-vm-database', passwd='vHhV8DfsSy2ZxA', db='movie', charset='utf8')
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



def get_proxy_url():
    url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=f66a6a47d0cf4daaaf9fd6c205f185c1&orderno=YZ20213303584Q5I9pq&returnType=2&count=1'
    response = requests.get(url)
    requests_json = json.loads(response.text)
    ips = requests_json['RESULT'][0]['ip'] + ':' + requests_json['RESULT'][0]['port']
    proxies = {
    "http": "http://{}".format(ips),
    "https": "https://{}".format(ips),
           }
    return proxies

proxy = get_proxy_url()

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
}
url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
response = requests.get(url, headers=headers, proxies=proxy)
html = etree.HTML(response.text)
arr = html.xpath('//table[@class="tagCol"]//td/a/text()')

try:
    for item in arr:
        url_item = 'https://book.douban.com/tag/' + item
        response_item = requests.get(url_item, headers=headers, proxies=proxy)
        if 'sorry' not in response.url:
            response_item_html = etree.HTML(response_item.text)
            next_url_page = response_item_html.xpath('//span[@class="next"]/a/@href')
            index = 1
            while index <= 50 and next_url_page:
                next_url = 'https://book.douban.com/' + next_url_page[0]
                index += 1
                response_item_index = requests.get(next_url, headers=headers, proxies=proxy)
                try:
                    if 'sorry' not in response_item_index.url:
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
                    else:
                        proxy = get_proxy_url()
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
                except:
                    proxy = get_proxy_url()
        else:
            proxy = get_proxy_url()
            url_item = 'https://book.douban.com/tag/' + item
            response_item = requests.get(url_item, headers=headers, proxies=proxy)
            response_item_html = etree.HTML(response_item.text)
            next_url_page = response_item_html.xpath('//span[@class="next"]/a/@href')
            index = 1
            while index <= 50 and next_url_page:
                next_url = 'https://book.douban.com/' + next_url_page[0]
                index += 1
                response_item_index = response_item = requests.get(next_url, headers=headers,
                                                                       proxies=proxy)
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
except:
    proxy = get_proxy_url()