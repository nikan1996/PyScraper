#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project_handler.py

@time: 2018/5/28 下午2:12
"""
from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.project import Project


class ProjectHandler:
    def get_all_projects(self):
        all = Project.query.filter_by(is_deleted=0).all()
        return convert_query_result2dict(all)
    
    def create_project(self, *, project_name, setting, cron_config, tag):
        project = Project(project_name=project_name, setting=setting, cron_config=cron_config, tag=tag)
        db.session.add(project)
        db.session.commit()
        return convert_query_result2dict(project)
    
    def get_project(self, project_id):
        return convert_query_result2dict(Project.query.filter_by(project_id=project_id, is_deleted=0).first())
    
    def delete_project(self, project_id):
        project = Project.query.filter_by(project_id=project_id, is_deleted=0).first()
        if project:
            project.is_deleted = 1
            db.session.commit()
        return convert_query_result2dict(project)
    
    def update_project(self, *, project_id, project_name, setting, cron_config, tag):
        project = Project.query.filter_by(project_id=project_id, is_deleted=0).first()
        if not project:
            return None
        project.project_name = project_name
        project.setting = setting
        project.cron_config = cron_config
        project.tag = tag
        db.session.add(project)
        db.session.commit()
        return convert_query_result2dict(project)
