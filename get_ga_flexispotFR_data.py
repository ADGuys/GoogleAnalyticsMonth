import datetime

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now() - datetime.timedelta(days=312))  # 111

profile_id = '236514082'  # 已经转化USD
source_name = 'FlexiSpotFR'
site_code = 'EU'
tool.get_data(start_time, today, profile_id, source_name, site_code)
