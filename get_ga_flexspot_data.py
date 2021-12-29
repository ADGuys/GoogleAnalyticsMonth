import datetime

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now() - datetime.timedelta(days=1433))

profile_id = '141269146'
source_name = 'FlexiSpot'
site_code = 'US'
tool.get_data(start_time, today, profile_id, source_name, site_code)
