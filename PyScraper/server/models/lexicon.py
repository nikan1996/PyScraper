#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: lexicon.py

@time: 2018/6/9 下午3:56
"""
import datetime
from sqlalchemy import text

from PyScraper.server.extensions import db


class GovLexicon(db.Model):
    __tablename__ = "gov_lexicon"
    
    rule_id = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="自增id")
    pattern = db.Column(db.String(191), doc="匹配pattern")
    correct_word = db.Column(db.String(191), doc="正确词")
    domain = db.Column(db.String(191), doc="域名")
    update_timestamp = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                                 doc="更新时间")
    create_timestamp = db.Column(db.TIMESTAMP, default=datetime.datetime.now, doc="创建时间")
