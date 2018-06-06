#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: base.py

@time: 2018/5/14 下午3:37
"""
import json

from flask_sqlalchemy import Model as ModelBase
from sqlalchemy import TypeDecorator, func
from sqlalchemy.dialects import mysql
from datetime import datetime

class BaseMixin(ModelBase):
    def as_dict(self):
        return {c.name: self.serialize(getattr(self, c.name)) for c in self.__table__.columns}
    
    def serialize(self, attr):
        if isinstance(attr, datetime):
            return str(attr)
        return attr

class JsonEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = mysql.LONGTEXT
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


def convert_query_result2dict(query_result):
    # convert to dict or list of dict
    if query_result is None:
        return query_result
    if isinstance(query_result, list):
        new_result = []
        for r in query_result:
            new_result.append(r.as_dict())
        return new_result
    else:
        return query_result.as_dict()
    

def get_count(q):
    # q:q = session.query(TestModel).filter(...).order_by(...)
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count