#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project.py

@time: 2018/5/14 下午4:20
"""
import datetime
from PyScraper.server.extensions import db
from PyScraper.server.models.base import JsonEncodedDict


class Project(db.Model):
    __tablename__ = "project"
    
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    project_name = db.Column(db.String(64), nullable=False, doc="项目名称")
    config = db.Column(JsonEncodedDict, doc="项目配置")
    tag = db.Column(db.String(64), doc="项目标签")
    is_deleted = db.Column(db.Boolean, default=0, doc="项目是否删除的标记")
    update_datetime = db.Column(db.DateTime, default=datetime.datetime.now, doc="更新时间")
    create_datetime = db.Column(db.DateTime, default=datetime.datetime.now, doc="创建时间")
    
    def __repr__(self):
        return "<Database %r>" % self.project_name