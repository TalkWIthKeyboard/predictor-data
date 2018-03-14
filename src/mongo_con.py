# coding=utf-8

import pymongo
import sys
import traceback

MONGODB_CONFIG = {
    'host': '122.152.219.33',
    'port': 27017,
    'db_name': 'passworddata',
    'username': 'passworddataOnwer',
    'password': 'hell0w0rld'
}

class MongoConn(object):
    def __init__(self):
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]
            self.username = MONGODB_CONFIG['username']
            self.password = MONGODB_CONFIG['password']

            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print traceback.format_exc()
            print 'Connect Mongodb Database Fail.'
            sys.exit(1)
