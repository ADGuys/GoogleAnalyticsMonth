import datetime
import time
import tool

today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
start_time = datetime.datetime(2018, 1, 6)
# start_time = (datetime.datetime.now() - datetime.timedelta(days=1484))

profile_id = '137390418'
source_name = 'Fleximounts'
site_code = 'US'

tool.get_data(start_time, today, profile_id, source_name, site_code)
