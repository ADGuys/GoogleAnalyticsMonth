import datetime

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = datetime.datetime(2021, 1, 13)

profile_id = '235675813'  # 已经转化USD
source_name = 'FlexiSpotES'
site_code = 'ES'
tool.get_data(start_time, today, profile_id, source_name, site_code)
