#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: task.py

@time: 2018/6/6 上午1:24
"""

import datetime

from sqlalchemy import text
from sqlalchemy.dialects.mysql import LONGTEXT
from PyScraper.server.extensions import db


class Task(db.Model):
    __tablename__ = "task"
    
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    project_id = db.Column(db.Integer, nullable=False, doc="项目id")
    url = db.Column(db.VARCHAR(2083), nullable=False, doc="项目爬取的URL")
    # redirect_url = db.Column(db.VARCHAR(2083), nullable=False, doc="项目重定向URL")
    status_code = db.Column(db.Integer, nullable=False, doc='状态码')
    reason = db.Column(db.VARCHAR(2000), nullable=True, doc='响应异常原因')
    content = db.Column(LONGTEXT, doc='网站源代码')
    update_timestamp = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                                 doc="更新时间")
    create_timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.now, doc="创建时间")
    # 创建复合索引
    __table_args__ = (db.Index('ix_project_name_update_timestamp', "project_id", "update_timestamp"),)
