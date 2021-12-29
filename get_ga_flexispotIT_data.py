import datetime

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now() - datetime.timedelta(days=80))  # 111

profile_id = '239678326'  # 已经转化USD
source_name = 'FlexiSpotIT'
site_code = 'IT'

tool.get_data(start_time, today, profile_id, source_name, site_code)

