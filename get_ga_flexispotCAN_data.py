import datetime

from googleapiclient.errors import HttpError

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now() - datetime.timedelta(days=238))  # 111

profile_id = '229460994'  # USD
source_name = 'FlexiSpotCAN'
site_code = 'CA'
try:
    tool.get_data(start_time, today, profile_id, source_name, site_code)
except HttpError as e:
    print('HttpError:' + e)
