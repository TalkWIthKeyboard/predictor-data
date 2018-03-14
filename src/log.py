# coding=utf-8

from datetime import datetime
import os

path = os.path.abspath('.')

class Log(object):
    @staticmethod
    def info(log_info):
        str = '[INFO] [{date}] {log_info}'.format(date=datetime.now(), log_info=log_info)
        print str
        with open('/Users/CoderSong/code/my-code/predictor-data/logs/info_log', 'a+') as f:
            f.write(str + '\n')

    @staticmethod
    def error(log_info):
        str = '[ERROR] [{date} {log_info}]'.format(date=datetime.now(), log_info=log_info)
        print str
        with open('/Users/CoderSong/code/my-code/predictor-data/logs/error_log', 'a+') as f:
            f.write(str + '\n')

    @staticmethod
    def warn(log_info):
        str = '[WARN] [{date}] {log_info}'.format(date=datetime.now(), log_info=log_info)
        print str
        with open('/Users/CoderSong/code/my-code/predictor-data/logs/warn_log', 'a+') as f:
            f.write(str + '\n')

    @staticmethod
    def celebrate(log_info):
        str = '[CELEBRATE] [{date}] {log_info}'.format(date=datetime.now(), log_info=log_info)
        print str
        with open('/Users/CoderSong/code/my-code/predictor-data/logs/celebrate_log', 'a+') as f:
            f.write(str + '\n')