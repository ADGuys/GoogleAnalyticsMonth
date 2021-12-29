import requests
import datetime
import time
import pymysql
import sys


# 数据处理
def rinse(json_s):
    keys = list(json_s)[-1]
    data_list = []
    # 跳出率
    if keys == 'bounce_rate':
        for i in json_s['bounce_rate']:
            date_time = i['date']
            br = i['bounce_rate']

            bounce_rate = "%.2f%%" % (br * 100)
            dict = {
                'date': date_time,
                'vl': bounce_rate
            }
            data_list.append(dict)
            # 访问量
    elif keys == 'visits':
        for i in json_s['visits']:
            date_time = i['date']
            dict = {
                'date': date_time,
                'vl': round(i['visits'])
            }
            data_list.append(dict)

    # 平均访问停留时间
    elif keys == 'average_visit_duration':
        for i in json_s['average_visit_duration']:
            date_time = i['date']
            tine_s = int(i['average_visit_duration'])
            seconds = int(tine_s)
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            dict = {
                'date': date_time,
                'vl': ("%d:%02d:%02d" % (h, m, s))
            }
            data_list.append(dict)

    # 全球排名
    elif keys == 'global_rank':
        for i in json_s['global_rank']:
            date_time = i['date']
            dict = {
                'date': date_time,
                'vl': round(i['global_rank'])
            }
            data_list.append(dict)

    # 国家排名
    elif keys == 'country_rank':
        for i in json_s['country_rank']:
            date_time = i['date']
            dict = {
                'date': date_time,
                'vl': round(i['country_rank'])
            }
            data_list.append(dict)

    # 每次访问页数
    else:
        for i in json_s['pages_per_visit']:
            date_time = i['date']
            dict = {
                'date': date_time,
                'vl': round(i['pages_per_visit'], 2)
            }
            data_list.append(dict)
    return data_list


# 获取上个月的第一天
def getNMonthBefore(date):
    month = date.month
    year = date.year
    for i in range(0):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    last_day = datetime.date(year, month, 1) - datetime.timedelta(1)
    first_day = datetime.date(last_day.year, last_day.month, 1)
    return first_day


# 数据存储和修改
def sql(com_url, site_url, dt, country):
    connect = pymysql.connect(host='east2-vm-database.mysql.database.chinacloudapi.cn', port=3306,
                              user='loctek@east2-vm-database', password='vHhV8DfsSy2ZxA', database='loctek_google_data',
                              charset='utf8')
    cursor = connect.cursor()
    url_list = (
        ("跳出率",
         "https://api.similarweb.com/v1/website/%s/total-traffic-and-engagement/bounce-rate?api_key=974a53ceeabe450cbb8084fd63dd03ff&start_date=%s&end_date=%s&country=%s&granularity=monthly&main_domain_only=false&format=json"),
        ('访问量',
         'https://api.similarweb.com/v1/website/%s/total-traffic-and-engagement/visits?api_key=974a53ceeabe450cbb8084fd63dd03ff&start_date=%s&end_date=%s&country=%s&granularity=monthly&main_domain_only=false&format=json'),
        ('每次访问页数',
         'https://api.similarweb.com/v1/website/%s/total-traffic-and-engagement/pages-per-visit?api_key=974a53ceeabe450cbb8084fd63dd03ff&start_date=%s&end_date=%s&country=%s&granularity=monthly&main_domain_only=false&format=json'),
        ('平均造访时间',
         'https://api.similarweb.com/v1/website/%s/total-traffic-and-engagement/average-visit-duration?api_key=974a53ceeabe450cbb8084fd63dd03ff&start_date=%s&end_date=%s&country=%s&granularity=monthly&main_domain_only=false&format=json&show_verified = false'),
        ('全球排名',
         'https://api.similarweb.com/v1/website/%s/global-rank/global-rank?api_key=974a53ceeabe450cbb8084fd63dd03ff&start_date=%s&end_date=%s&main_domain_only=false&format=json'),
        ('国家排名',
         'https://api.similarweb.com/v1/website/%s/country-rank/country-rank?api_key=974a53ceeabe450cbb8084fd63dd03ff&start_date=%s&end_date=%s&country=%s&main_domain_only=false&format=json')
    )
    payload = {}
    headers = {}
    for urls in url_list:
        # dt = getNMonthBefore(date_d)
        dt = '2021-01-01'
        try:
            url = (urls[1]) % (com_url, dt, dt, country)
        except:
            url = (urls[1]) % (com_url, dt, dt)
        name = urls[0]
        req = requests.get(url, headers=headers, data=payload).json()
        if req['meta']['status'] == 'Error':
            print('------ 数据可能未更新，程序自动退出，请推迟一天运行 ------')
            sys.exit(0)
        else:
            print(name)
            # print(req)
            try:

                datas = rinse(req)
                for i in datas:
                    date_month = i['date']
                    data = i['vl']
                    print(data)
                    if name == '访问量':
                        sql = """ UPDATE similarweb SET total_visits= %s  WHERE date = %s and site_name = %s and country = %s"""
                        var = (data, dt, site_url, country)
                        cursor.execute(sql, var)
                        connect.commit()
                        print('<<<<<<<<<<<<<<<<<<< 添 加 数 据')

                    elif name == '跳出率':
                        sql = """ UPDATE similarweb SET bounce_rate= %s  WHERE  date = %s and site_name = %s and country = %s"""
                        var = (data, dt, site_url, country)
                        cursor.execute(sql, var)
                        connect.commit()
                        print('<<<<<<<<<<<<<<<<<<< 添 加 数 据')

                    elif name == '每次访问页数':
                        sql = """ UPDATE similarweb SET pages_per_visit= %s WHERE  date = %s and site_name = %s and country = %s"""
                        var = (data, dt, site_url, country)
                        cursor.execute(sql, var)
                        connect.commit()
                        print('<<<<<<<<<<<<<<<<<<< 添 加 数 据')

                    elif name == '平均造访时间':
                        sql = """ UPDATE similarweb SET average_visit_duration= %s WHERE  date = %s and site_name = %s and country = %s"""
                        var = (data, dt, site_url, country)
                        cursor.execute(sql, var)
                        connect.commit()
                        print('<<<<<<<<<<<<<<<<<<< 添 加 数 据')

                    elif name == '全球排名':
                        sql = """ UPDATE similarweb SET global_rank= %s WHERE  date = %s and site_name = %s and country = %s"""
                        var = (data, dt, site_url, country)
                        cursor.execute(sql, var)
                        connect.commit()
                        print('<<<<<<<<<<<<<<<<<<< 添 加 数 据')

                    elif name == '国家排名':
                        sql = """ UPDATE similarweb SET country_rank= %s  WHERE date = %s and site_name = %s and country = %s"""
                        var = (data, dt, site_url, country)
                        cursor.execute(sql, var)
                        connect.commit()
                        print('<<<<<<<<<<<<<<<<<<< 添 加 数 据')
                # return 'ok'
            except:
                print('程序内部错误，可能出现了小BUG')
                sys.exit(0)


# 处理请求数据
def red_req():
    # 当前时间
    date_d = datetime.datetime.now()
    com_list = (
        ('bauhutte.jp', 'JP', '392', '日本'),
        ('ergotopia.de', 'DE', '276', '德国'),
        ('bohomoebel.de', 'DE', '276', '德国'),
        ('ergodesks.co.uk', 'UK', '826', '英国'),
        ('de.flexispot.com', 'DE', '276', '德国'),
        ('flexispot.co.uk', 'UK', '826', '英国'),
        ('fr.flexispot.com', 'FR', '250', '法国'),
        ('flexispot.JP', 'JP', '392', '日本'),
        ('flexispot.com', 'US', '840', '美国'),
        ('autonomous.ai', 'US', '840', '美国'),
        ('fully.com', 'US', '840', '美国'),
        ('upliftdesk.com', 'US', '840', '美国'),
        ('flexispot.ca', 'CA')
    )
    for site_title in com_list:
        com_url = site_title[0]
        country = site_title[1]
        site_url = max(com_url.split('.'), key=len, default='')
        # 当前日期
        t = int(time.time())
        # now_date = int(round(t * 1000))
        dt = getNMonthBefore(date_d)
        # dt = '2021-01-01'
        connect = pymysql.connect(host='east2-vm-database.mysql.database.chinacloudapi.cn', port=3306,
                                  user='loctek@east2-vm-database', password='vHhV8DfsSy2ZxA',
                                  database='loctek_google_data', charset='utf8')
        cursor = connect.cursor()
        sqls = '''select * from similarweb where date = %s and site_name = %s and country =%s'''
        var = (dt, site_url, country)
        cursor.execute(sqls, var)
        results1 = cursor.fetchall()
        results = len(results1)
        if results == 0:
            cursor.execute(
                """insert into similarweb(date,site_name,country) value ("{}","{}","{}")""".format(dt, site_url,
                                                                                                   country))
            connect.commit()
            print('----------', site_url, '-----------')
            print('----------------添 加 数据------------------')
            sql(com_url, site_url, dt, country)

        else:
            print('----------------更 新 数据------------------')
            sql(com_url, site_url, dt, country)


if __name__ == '__main__':
    red_req()
