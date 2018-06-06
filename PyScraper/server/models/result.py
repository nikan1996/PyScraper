#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: result.py

@time: 2018/6/6 上午1:27
"""

import datetime

from sqlalchemy import text
from sqlalchemy.dialects import mysql

from PyScraper.server.extensions import db


class Result(db.Model):
    __tablename__ = "result"
    
    result_id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    project_id = db.Column(db.Integer, nullable=False, doc="项目名称")
    
    result = db.Column(mysql.JSON, doc="爬取结果")
    update_timestamp = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                                 doc="更新时间", index=True)
    create_timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.now, doc="创建时间")
    # 创建复合索引
    __table_args__ = (db.Index('ix_project_name_update_timestamp', "project_id", "update_timestamp"),)
