import datetime

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now() - datetime.timedelta(days=1000))

profile_id = '170556909'
source_name = 'FlexiSpotJP'
site_code = 'JP'
tool.get_data(start_time, today, profile_id, source_name, site_code)
