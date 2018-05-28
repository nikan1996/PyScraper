#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: database_handler.py

@time: 2018/5/14 下午2:54
"""
import datetime

from sqlalchemy import text

from PyScraper.server.extensions import db
from PyScraper.server.models.base import JsonEncodedDict

from sqlalchemy.dialects import mysql

class Database(db.Model):
    __tablename__ = "database"
    
    database_id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    database_name = db.Column(db.String(64), nullable=False, doc="数据库名称")
    config = db.Column(mysql.JSON, doc="数据库配置")
    is_deleted = db.Column(db.Boolean, default=0, doc="数据库是否删除的标记")
    update_timestamp = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), doc="更新时间")
    create_timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, doc="创建时间")