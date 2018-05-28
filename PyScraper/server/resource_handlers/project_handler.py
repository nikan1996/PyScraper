#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project_handler.py

@time: 2018/5/28 下午2:12
"""
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.project import Project


class ProjectHandler:
    def get_all_projects(self):
        all = Project.query.all()
        return convert_query_result2dict(all)
    
    def get_project(self, project_id):
        return convert_query_result2dict(Project.query.filter_by(project_id=project_id).first())
    
    def delete_project(self, project_id):
        return project_id
    
    def update_project(self, project_id, ):
        project = Project.query.filter_by(project_id=project_id).first()
        return convert_query_result2dict(project)
    
    
    
        
