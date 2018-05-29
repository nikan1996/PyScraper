#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: config.py

@time: 2018/5/14 下午3:44
"""


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/pyscraper'
    
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/test_pyscraper'
