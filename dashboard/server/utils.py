# -*- coding: utf-8 -*-

import os
import time
import json
import random
from functools import wraps

import MySQLdb
import pandas as pd
from flask import make_response, jsonify


def build_response(content, code=200):
    """
    Build response, add headers
    """
    response = make_response(jsonify(content), content['code'])
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    return response


color_set = {
    "red": u"\033[1;31m{}\033[0m", "green": u"\033[1;32m{}\033[0m",
    "yellow": u"\033[1;33m{}\033[0m", "blue": u"\033[1;34m{}\033[0m",
    "magenta": u"\033[1;35m{}\033[0m", "cyan": u"\033[1;36m{}\033[0m",
    "white": u"\033[1;37m{}\033[0m",
}


def print_info(text, color='white', kill=False):
    global color_set
    print('color:', color)
    template = color_set.get(color)
    print(template.format(text))
    if kill:
        exit(-1)


def print_func_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('\n###start run fun:  {} ...'.format(func.__name__))
        result = func(*args, **kwargs)
        print('\n###finish run fun:  {} ...'.format(func.__name__))
        return result
    return wrapper


class Map(dict):
    """
    示例:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    # 添加
    m.new_key = 'Hello world!'
    m['new_key'] = 'Hello world!'
    print(m.new_key)
    print(m['new_key'])
    # 更新
    m.new_key = 'Yay!'
    m['new_key'] = 'Yay!'
    # 删除
    del m.new_key
    del m['new_key']
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class SQL(object):
    __metaclass__ = Singleton

    def __init__(self, host, port, user, passwd, db):
        super(SQL, self).__init__()
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                    db=self.db)

    def get_conn(self):
        try:
            self.conn.stat()
        except:
            self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                        db=self.db)

        return self.conn

    def run(self, sql):
        self.get_conn()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        if cursor.description:
            columns = [i[0] for i in cursor.description]
            frame = pd.DataFrame.from_records(list(result), columns=columns)
            return frame.to_dict()

        return None
