#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: task_handler.py

@time: 2018/6/6 上午2:07
"""
from sqlalchemy import func

from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.task import Task


class TaskHandler:
    def get(self, project_id, limit=10, offset=0):
        all = Task.query.filter_by(project_id=project_id).order_by(
            Task.update_timestamp.desc()).limit(limit).offset(offset).all()
        all_dict = convert_query_result2dict(all)
        result = {
            'total_count': self.count(project_id=project_id),
            'count': len(all),
            'result': all_dict,
        }
        return result
    
    def put_newtask(self, project_id, url, content, status_code, reason=None):
        new_task = Task(project_id=project_id, url=url, content=content, status_code=status_code, reason=reason)
        db.session.add(new_task)
        db.session.commit()
        return project_id
    
    def count(self, project_id=None):
        if project_id:
            return db.session.query(func.count(Task.task_id)).filter_by(project_id=project_id).scalar()
        else:
            return db.session.query(func.count(Task.task_id)).scalar()


