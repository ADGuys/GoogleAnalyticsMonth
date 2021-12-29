import datetime

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = (datetime.datetime.now() - datetime.timedelta(days=300))  # 111

profile_id = '235700456'  # USD
source_name = 'FlexiSpotUK'
site_code = 'EU'
tool.get_data(start_time, today, profile_id, source_name, site_code)
