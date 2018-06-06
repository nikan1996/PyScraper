#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: result_handler.py

@time: 2018/6/6 上午2:07
"""
from sqlalchemy import func

from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.result import Result


class ResultHandler:
    def get(self, project_id, limit=10, offset=0):
        all = Result.query.filter_by(project_id=project_id).order_by(
           Result .update_timestamp.desc()).limit(limit).offset(offset).all()
        all_dict = convert_query_result2dict(all)
        result = {
            'total_count': self.count(project_id=project_id),
            'count': len(all),
            'result': all_dict,
        }
        return result
    
    def put_result(self, project_id, result):
        result = Result(project_id=project_id, result=result)
        db.session.add(result)
        db.session.commit()
        return project_id
    
    def count(self, project_id):
        if project_id:
            return db.session.query(func.count(Result.result_id)).filter_by(project_id=project_id).scalar()
        else:
            return db.session.query(func.count(Result.result_id)).scalar()
