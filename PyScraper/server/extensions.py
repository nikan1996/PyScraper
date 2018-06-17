#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: extensions.py

@time: 2018/5/14 下午3:38
"""
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from PyScraper.server.models.base import BaseMixin
# from PyScraper.utils.multiprocessing_queue import Queue
from queue import Queue

db = SQLAlchemy(session_options={'autocommit': False}, model_class=BaseMixin)
spidercls_queue = Queue()

auth = HTTPBasicAuth()
users = {
    "wenzhou": "wenzhou",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

