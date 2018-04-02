# coding=utf-8

from src.mysql_con import MysqlConn
from src.mongo_con import MongoConn

mongo_db = MongoConn()
mysql_db = MysqlConn()

db_table_name = ['t12306', '7k7k', 'duduniu', 'phpbb', 'rock', 'tianya']

# 统计合法数据
def stat_legal_data():
    legal_data = {}
    for each in db_table_name:
        legal_data[each] = {}
        sql_str = 'SELECT COUNT(*) FROM {table}'.format(table=each)
        legal_data[each]['total_num'] = mysql_db.excuse(sql_str)[0][0]
        legal_data[each]['legal_num'] = mongo_db.db['info'].find({'source': each}).count(True)
    legal_data['source'] = 'legal_data'
    mongo_db.db['statistic'].insert(legal_data)

if __name__ == '__main__':
    stat_legal_data()


