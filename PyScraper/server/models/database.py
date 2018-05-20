#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: database.py

@time: 2018/5/14 下午2:54
"""
import datetime

from PyScraper.server.extensions import db
from PyScraper.server.models.base import JsonEncodedDict


class Database(db.Model):
    __tablename__ = "database"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    database_name = db.Column(db.String(64), nullable=False, doc="数据库名称")
    config = db.Column(JsonEncodedDict, doc="数据库配置")
    is_deleted = db.Column(db.Boolean, default=0, doc="数据库是否删除的标记")
    update_datetime = db.Column(db.DateTime, default=datetime.datetime.now, doc="更新时间")
    create_datetime = db.Column(db.DateTime, default=datetime.datetime.now, doc="创建时间")
    
    def __repr__(self):
        return '<Database %r>' % self.database_name
