#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project.py

@time: 2018/5/14 下午4:20
"""
import datetime

from sqlalchemy import text
from sqlalchemy.dialects import mysql

from PyScraper.server.extensions import db


class Project(db.Model):
    __tablename__ = "project"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    project_name = db.Column(db.String(191), nullable=False, doc="项目名称")
    setting = db.Column(mysql.JSON, doc="项目配置")
    
    cron_config = db.Column(mysql.JSON, doc="项目调度配置")
    tag = db.Column(db.String(191), doc="项目标签")
    is_deleted = db.Column(db.Boolean, default=0, doc="项目是否删除的标记")
    update_timestamp = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), doc="更新时间")
    create_timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.now, doc="创建时间")

