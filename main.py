import json
import requests
import re
import pymysql as mdb
import random
from lxml import etree
from langconv import *
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
}
conn = mdb.connect(host='east2-vm-database.mysql.database.chinacloudapi.cn', port=3306,
                   user='loctek@east2-vm-database',
                   passwd='vHhV8DfsSy2ZxA', db='movie', charset='utf8')
cursor = conn.cursor()


def not_empty(s):
    list_s = []
    for i in s:
        list_s.append(''.join(i.strip()))
    return list_s


# 合并列表里的元素
def merge(list_s):
    k = 0
    a_str = ' '
    while k < len(list_s):
        a_str = a_str + str(list_s[k])
        k += 1
    return a_str.replace('\r', '').replace('\n', '').replace('\t', '')


def get_proxy_url():
    time.sleep(5)
    print(1)
    url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=88cbe1d214ea4cc294c23e6416ce4a16&orderno=YZ20213235042UDxiik&returnType=2&count=1'
    response = requests.get(url)
    requests_json = json.loads(response.text)
    ips = requests_json['RESULT'][0]['ip'] + ':' + requests_json['RESULT'][0]['port']
    proxies = {
        "http": "http://{}".format(ips),
        "https": "https://{}".format(ips),
    }
    print(proxies)
    return proxies


def Traditional2Simplified(text):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", text)
    sentence = Converter('zh-hans').convert(sub_str)
    return sentence


def get_data(num):
    num = num * 200
    cursor.execute('select * from douban_book limit {}, 200'.format(num))
    data = cursor.fetchall()
    print(num)
    return data


proxy = get_proxy_url()
# print(proxy)

num = 148
while True:
    data = get_data(num)
    for item in data:
        try:
            url = item[1]
            type = item[2]
            # print(proxy, 123123, url)

            req = requests.get(url, headers=headers, timeout=7, proxies=proxy)
            req_html = etree.HTML(req.text)
            title = req_html.xpath('//span[@property="v:itemreviewed"]/text()')[0]
            title_list = etree.HTML(req.text).xpath('//*[@id="info"]//text()')
            # 图片
            try:
                img = etree.HTML(req.text).xpath('//*[@id="mainpic"]/a/img/@src')[0]
            except:
                img = ''
            # 评分
            try:
                shar = etree.HTML(req.text).xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
            except:
                shar = ''
            txt = merge(not_empty(title_list))
            # 作者
            try:
                types = re.findall("作者:(.*?)出版社", txt)[0]
            except:
                types = ''
            # 出版社
            try:
                try:
                    press = re.findall("出版社:(.*?)原作名", txt)
                except:
                    press = re.findall("出版社:(.*?)出品方", txt)
                try:
                    press = re.findall("出版社:(.*?)出版年", txt)
                except:
                    press = re.findall("出版社:(.*?)页数", txt)
                if press == []:
                    press = re.findall("出版社:(.*?)副标题", txt)
                if press == []:
                    press = re.findall("出版社:(.*?)装帧", txt)
            except:
                press = ['']
            if press == []:
                press = ['']
            print(press)
            # # 出版年
            try:
                try:
                    sketchy = re.findall("出版年:(.*?)页数", txt)[0]
                except:
                    sketchy = re.findall("出版年:(.*?)定价", txt)[0]
            except:
                sketchy = ''
            try:
                label = etree.HTML(req.text).xpath('//*[@id="db-tags-section"]/div/span/a/text()')
            except:
                label = ''
            arrest = "/".join(label)
            spare = type + "/" + arrest
            # 内容简介
            theory = etree.HTML(req.text).xpath('//*[@id="link-report"]/div[1]/div/p/text()')
            if theory == []:
                theory = etree.HTML(req.text).xpath('//*[@id="link-report"]/span[1]/div/p/text()')
            # 作者简介
            play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/div/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/span[1]/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//*[@id="content"]/div/div[1]/div[3]/div[2]/span[1]/div/p/text()')
            if play == []:
                play = etree.HTML(req.text).xpath('//div[@class="indent "]/span[@class="short"]/div/p/text()')
            content = merge(not_empty(theory))  # 内容简介
            author = merge(not_empty((play)))  # 作者简介
            print(types)
            print(sketchy)
            print(content)
            print(author)
            print(spare)
            if types:
                author_copy = Traditional2Simplified(types)
            else:
                author_copy = ''
            if title:
                title_copy = Traditional2Simplified(title)
            else:
                title_copy = ''
            if press:
                press = press[0]
            else:
                press = ''
            source = '豆瓣书籍'
            try:
                cursor = conn.cursor()
                print(types, title, 123)
                sqls = '''select * from echo_loctek_douban_books where author = %s and title = %s'''
                va = (types, title)
                cursor.execute(sqls, va)
                results1 = cursor.fetchall()
                results = len(results1)
                if results == 0:
                    sql = 'insert into echo_loctek_douban_books(title, img, content, author, brief, rate, be_on, source, cate, press, author_copy, title_copy) value("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
                        title, img, content, types, author, shar, sketchy, source,
                        spare,
                        press, author_copy, title_copy)
                    # 提交sql语句，映射到数据库中。
                    cursor.execute(sql)
                    conn.commit()
                    print('插入')
                    print('num:', num)
                else:
                    pass
            except:
                pass
        except:
            proxy = get_proxy_url()
    num += 1
#
