from logging import log

import pymysql


# 'abs3': 'mysql+pymysql://loctekroot@old-db-abs56:FHY7LEVv*G*#%K&@@old-db-abs56.mysql.database.azure.com/abs3',

class DBPipeline:
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='old-db-abs56.mysql.database.azure.com',
            port=3306,
            db='abs3',
            user='loctekroot@old-db-abs56',
            passwd='FHY7LEVv*G*#%K&@',
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item):
        try:
            # 查重处理
            self.cursor.execute(
                """select * from google_analytics_flow where date = %s and source_name = %s""",
                (item['date'],
                 item['source_name']
                 ))
            # 是否有重复数据
            repetition = self.cursor.fetchone()
            # 重复
            if repetition:
                sql = '''
                UPDATE google_analytics_flow 
                SET UV = %s, PV = %s, organic_search = %s, paid_search = %s, direct = %s, referral = %s, email = %s, social = %s, other = %s, transactionsPerSession = %s,avgTimeOnPage = %s,transactions=%s,sessions=%s,revenue=%s,bounces=%s,site_code=%s
                WHERE date = %s and source_name = %s
                  '''

                val = (
                    item['UV'], item['PV'], item['organic_search'], item['paid_search'], item['direct'],
                    item['referral'],
                    item['email'], item['social'],
                    item['other'],
                    item['transactionsPerSession'], item['avgTimeOnPage'], item['transactions'], item['sessions'],
                    item['transactionRevenue'], item['bounces'], item['site_code'],
                    item['date'], item['source_name'])

                self.cursor.execute(sql, val)
                self.connect.commit()

            else:
                # 插入数据
                self.cursor.execute(
                    """insert into google_analytics_flow(UV, PV, organic_search, paid_search, direct, referral, email, social, other, date, source_name,transactionsPerSession,avgTimeOnPage,transactions,sessions,revenue,bounces,site_code)
                    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)""",
                    (item['UV'],
                     item['PV'],
                     item['organic_search'],
                     item['paid_search'],
                     item['direct'],
                     item['referral'],
                     item['email'],
                     item['social'],
                     item['other'],
                     item['date'],
                     item['source_name'],
                     item['transactionsPerSession'],
                     item['avgTimeOnPage'],
                     item['transactions'],
                     item['sessions'],
                     item['transactionRevenue'],
                     item['bounces'],
                     item['site_code']
                     )
                )

                # 提交sql语句
                self.connect.commit()

        except Exception as error:
            print(error)
            # 出现错误时打印错误日志
            pass
        return item
