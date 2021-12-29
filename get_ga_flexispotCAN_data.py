import datetime

from googleapiclient.errors import HttpError

import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = datetime.datetime(2020, 9, 26)

profile_id = '229460994'  # USD
source_name = 'FlexiSpotCAN'
site_code = 'CA'
tool.get_data(start_time, today, profile_id, source_name, site_code)
