#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: config.py

@time: 2018/5/14 下午3:44
"""


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/pyscraper'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_POOL_SIZE = 3
    # By default, MariaDB is configured to have a 600 second timeout.
    # it is recommended that you set SQLALCHEMY_POOL_RECYCLE to a value less than your backend’s timeout.
    SQLALCHEMY_POOL_RECYCLE = 600
    
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/test_pyscraper'
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_RECYCLE = 600