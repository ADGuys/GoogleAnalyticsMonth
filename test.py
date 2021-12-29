import datetime

import tool
from apscheduler.schedulers.blocking import BlockingScheduler

# def my_clock():
#     print('hello world')
#
#
# if __name__ == '__main__':
#     scheduler = BlockingScheduler()
#     scheduler.add_job(my_clock, 'interval', hours=1)
#     scheduler.start()

def ga_task():
    site_code_dict = {
        'Fleximounts': 'US',
        'FlexiSpot': 'US',
        'FlexiSpotUK': 'EU',
        'FlexiSpotDE': 'EU',
        'FlexiSpotFR': 'EU',
        'FlexiSpotJP': 'JP',
        'FlexiSpotCAN': 'CA',
        'FlexiSpotIT': 'IT',
        'FlexiSpotES': 'ES',
    }
    tmp_dic = {
        'Fleximounts': '137390418',
        'FlexiSpotCAN': '228967663',
        'FlexiSpotDE': '179192080',
        'FlexiSpotJP': '170556909',
        'FlexiSpotUK': '178999234',
        'FlexiSpot': '141269146',
        'FlexiSpotIT': '239678326',
        'FlexiSpotES': '235675813',
        'FlexiSpotFR': '236514082',
    }
    today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    start_time = (datetime.datetime.now() - datetime.timedelta(days=5))
    for k, v in tmp_dic.items():
        site_code = site_code_dict[k]
        tool.get_data(start_time, today, v, k, site_code)



# 07

if __name__ == '__main__':
    ga_task()
    scheduler = BlockingScheduler()
    scheduler.add_job(ga_task, 'interval', hours=1)
    scheduler.start()
