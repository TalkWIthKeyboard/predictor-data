# coding=utf-8

from mysql_con import MysqlConn
from mongo_con import MongoConn
from log import Log
from parser import Parser, Check
import traceback


sql_list = {
    'count': 'SELECT COUNT(*) FROM {table}',
    'itr_all': 'SELECT {query_schema} FROM {table} ' +
                'WHERE id >= (SELECT id FROM {table} ORDER BY id LIMIT {start}, 1) ' +
                'ORDER BY id LIMIT 10000',
}

db_useful_schema = {
    't12306': ['password', 'email', 'name', 'CtfID', 'mobile', 'username'],
    '7k7k': ['password', 'username'],
    'duduniu': ['password', 'username', 'email'],
    'phpbb': ['password', 'numcount'],
    'rock': ['password', 'numcount'],
    'tianya': ['password', 'email', 'username']
}

db_table_name = ['t12306', '7k7k', 'duduniu', 'phpbb', 'rock', 'tianya']
db_rubbish_box = {}
db_repetition_box = {}
db_hash_map = {}

for name in db_table_name:
    db_rubbish_box[name] = 0
    db_repetition_box[name] = 0
    db_hash_map[name] = {}

def dataPaser(data, table):
    mongo_array = []
    for each in data:
        try:
            if len(each[0]) >= 3 and len(each[0]) <= 30 and Check.password(each[0]):
                if not db_hash_map[table].has_key(str(hash(each))):
                    db_hash_map[table][str(hash(each))] = True
                    if table == 't12306':
                        mongo_data = Parser.p_t12306(each)
                    if table == '7k7k':
                        mongo_data = Parser.p_7k7k(each)
                    if table == 'duduniu':
                        mongo_data = Parser.p_duduniu(each)
                    if table == 'phpbb' or table == 'rock':
                        mongo_data = Parser.p_phpbb_rock(each, table)
                    if table == 'tianya':
                        mongo_data = Parser.p_tianya(each)
                    mongo_array.append(mongo_data)
                else:
                    db_repetition_box[table] += 1
            else:
                db_rubbish_box[table] += 1
        except Exception:
            Log.error('The data in {table} has some problem: {data}'.format(table=table, data=each))
    mongo_db.db['info'].insert(mongo_array)

if __name__ == '__main__':
    mongo_db = MongoConn()
    mysql_db = MysqlConn()

    # 清洗数据，转到mongodb
    for table, schema_list in db_useful_schema.items():
        count = mysql_db.excuse(sql_list['count'].format(table=table))
        count = count[0][0]
        index_start = 0
        while index_start < count:
            try:
                query_schema = ''
                for index in range(len(schema_list)):
                    if index < len(schema_list) - 1:
                        query_schema += schema_list[index] + ','
                    else:
                        query_schema += schema_list[index]
                data = mysql_db.excuse(sql_list['itr_all'].format(
                    query_schema=query_schema,
                    table=table,
                    start=index_start
                ))
                dataPaser(data, table)
                index_start += len(data)
                Log.info('Finished to save mongo data in {table} {num}/{count}'
                         .format(table=table, num=index_start, count=count))
            except Exception:
                print traceback.format_exc()
        Log.celebrate('The data in {table} has already saved in mongo, rubbish: {rubbish}, repetition: {repetition}'
                      .format(table=table, rubbish=db_rubbish_box[table], repetition=db_repetition_box[table]))

    # 保存一些统计数据
    db_rubbish_box['source'] = 'rubbish'
    db_repetition_box['source'] = 'repetition'
    mongo_db.db['statistic'].insert([db_rubbish_box, db_repetition_box])
