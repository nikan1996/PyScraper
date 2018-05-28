#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: extensions.py

@time: 2018/5/14 下午3:38
"""

from flask_sqlalchemy import SQLAlchemy
from PyScraper.server.models.base import BaseMixin
from PyScraper.utils.multiprocessing_queue import Queue

db = SQLAlchemy(model_class=BaseMixin)
queue = Queue()