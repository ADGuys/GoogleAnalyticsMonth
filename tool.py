import json
import datetime
import calendar
from dateutil.relativedelta import relativedelta

import install_ga_demo as gaapi

from db.mysql_helper import DBPipeline


def get_end_time(start_time):
    assert isinstance(start_time, datetime.datetime), 'start time error not type:datetime'
    years = start_time.year
    months = start_time.month
    end_day = calendar.monthrange(years, months)
    end_time = datetime.datetime(years, months, end_day[1])
    return end_time


def get_data(start_time, today, profile_id, source_name, site_code):
    key_file_location = 'blissful-answer-260301-e3ed7a61b33e.json'
    scope = ['https://www.googleapis.com/auth/analytics']
    service = gaapi.get_service('analytics', 'v3', scope, key_file_location)
    while start_time.strftime("%Y-%m-%d") > today:
        end_date = get_end_time(start_time)
        start_date = start_time.strftime("%Y-%m-%d")

        data = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start_date,
            end_date=end_date,
            max_results='100',
            metrics='ga:users',
            dimensions='ga:channelGrouping',
            sort='ga:users'
        ).execute()

        temp_dic = {}
        if data.get('rows', 0):
            for tmp_list in data['rows']:
                temp_dic.update({
                    tmp_list[0]: tmp_list[1]
                })
            arg = {
                'paid_search': temp_dic.pop('Paid Search', 0),
                'direct': temp_dic.pop('Direct', 0),
                'organic_search': temp_dic.pop('Organic Search', 0),
                'referral': temp_dic.pop('Referral', 0),
                'social': temp_dic.pop('Social', 0),
                'email': temp_dic.pop('Email', 0),
                'other': temp_dic.pop('(Other)', 0),
            }
        else:
            print('没有搜索数据')

        data = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start_date,
            end_date=end_date,
            max_results='100',
            metrics='ga:users, ga:Pageviews, ga:transactionsPerSession, ga:avgTimeOnPage, ga:transactions, ga:sessions, ga:transactionRevenue,ga:bounces',
            # dimensions='ga:medium',
            sort='ga:users'
        ).execute()

        temp_dic = {}
        if data.get('rows', 0):
            arg.update({
                'UV': data['rows'][0][0],
                'PV': data['rows'][0][1],
                'transactionsPerSession': data['rows'][0][2],
                'avgTimeOnPage': data['rows'][0][3],
                'transactions': data['rows'][0][4],
                'sessions': data['rows'][0][5],
                'transactionRevenue': data['rows'][0][6],
                'bounces': data['rows'][0][7],
                'date': start_date,
                'source_name': source_name,
                'site_code': site_code,
            })
            print(arg)
        else:
            print('没有访客记录')
        next_start_time = start_time + relativedelta(months=1)
        start_time = datetime.datetime(next_start_time.year, next_start_time.month, 1)
        DBPipeline().process_item(arg)
