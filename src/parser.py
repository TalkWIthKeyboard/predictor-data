# coding=utf-8

import re
import string

class Check:
    @staticmethod
    def password(pwd):
        return re.match(r'^[{punctuation}0-9a-zA-Z]*$'.format(punctuation=string.punctuation), pwd)

    @staticmethod
    def mail(mail):
        return re.match(r'^[0-9a-zA-Z_,]*@[0-9a-zA-Z]*.[0-9a-zA-Z]*$'.format(punctuation=string.punctuation), mail)

    @staticmethod
    def username(username):
        return re.match(r'.*\?{3}.*', username)

class Parser:
    @staticmethod
    def p_t12306(data):
        mongo_data = {}
        # 身份证号码15位,18位
        ctfid = data[3] if len(data[3]) == 15 or len(data[3]) == 18 else None
        mongo_data['password'] = data[0]
        if Check.mail(data[1]):
            mongo_data['email'] = data[1]
        # 去除某些名字中含有特殊标点符号和空格
        mongo_data['name'] = unicode(data[2].encode('utf-8').translate(None, string.punctuation).replace(' ', ''),
                                     'utf-8')
        if ctfid:
            mongo_data['birthday'] = ctfid[6:14] if len(ctfid) == 18 else ctfid[6:12]
        # 电话号码11位
        if len(data[4]) == 11:
            mongo_data['mobile'] = data[4]
        mongo_data['username'] = data[5]
        mongo_data['source'] = 't12306'
        return mongo_data

    @staticmethod
    def p_7k7k(data):
        mongo_data = {}
        mongo_data['password'] = data[0]
        if Check.mail(data[1]):
            mongo_data['email'] = data[1]
        mongo_data['source'] = '7k7k'
        return mongo_data

    @staticmethod
    def p_duduniu(data):
        mongo_data = {}
        mongo_data['password'] = data[0]
        mongo_data['username'] = data[1]
        email = data[2].replace('"', '').replace('[', '').replace(']', '')
        if Check.mail(email):
            mongo_data['email'] = email
        mongo_data['source'] = 'duduniu'
        return mongo_data

    @staticmethod
    def p_phpbb_rock(data, table):
        mongo_data = {}
        mongo_data['password'] = data[0]
        mongo_data['numcount'] = data[1]
        mongo_data['source'] = table
        return mongo_data

    @staticmethod
    def p_tianya(data):
        mongo_data = {}
        mongo_data['password'] = data[0]
        if Check.mail(data[1]):
            mongo_data['email'] = data[1]
        if not Check.username(data[2]):
            mongo_data['username'] = data[2]
        mongo_data['source'] = 'tianya'
        return mongo_data
