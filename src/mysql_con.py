# coding=utf-8

import MySQLdb
import sys
import traceback

MYSQL_CONFIG = {
    'host': '10.60.39.19',
    'db_name': 'passworddata',
    'username': 'root',
    'password': 'mysql_pass'
}

class MysqlConn(object):
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(
                MYSQL_CONFIG['host'],
                MYSQL_CONFIG['username'],
                MYSQL_CONFIG['password'],
                MYSQL_CONFIG['db_name'],
                charset="utf8"
            )
            self._cursor = self.conn.cursor()
        except Exception:
            print traceback.format_exc()
            print 'Connect Mysql Database Fail.'
            sys.exit(1)

    def excuse(self, query):
        try:
            cursor = self._cursor
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            print traceback.format_exc()
