#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: base.py

@time: 2018/5/14 下午3:37
"""
import json

from flask_sqlalchemy import Model as ModelBase
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects import mysql


class BaseMixin(ModelBase):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    
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
