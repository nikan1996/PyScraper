#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project_handler.py

@time: 2018/5/28 下午2:12
"""
from PyScraper.server.extensions import db
from PyScraper.server.extensions import spidercls_queue
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.project import Project
from PyScraper.utils import create_script


class ProjectHandler:
    def get_all_projects(self):
        all = Project.query.filter_by(is_deleted=0).all()
        return convert_query_result2dict(all)
    
    def create_project(self, *, project_name, setting, cron_config, tag):
        if not setting.get('spidercls'):
            spider_name = setting.get('spider_name')
            rules = setting.get('rules')
            start_url = setting.get('start_url')
            mail_to = setting.get('information_config').get('email')
            script_type = setting.get('script_type')
            spidercls = create_script(script_name=spider_name, rules=rules, start_url=start_url, mail_to=mail_to,
                                      script_type=script_type)
            setting['spidercls'] = spidercls
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
        db.session.commit()
        return convert_query_result2dict(project)
    
    def update_project_status(self, project_id, status):
        project = Project.query.filter_by(project_id=project_id, is_deleted=0).first()
        if project:
            project.status = status
            db.session.commit()
        return convert_query_result2dict(project)


class ProjectActionHandler:
    START = 'start'
    PAUSE = 'pause'
    STOP = 'stop'
    
    def put_item_into_spider_loop(self, project_id, action):
        project = Project.query.filter_by(project_id=project_id, is_deleted=0).first()
        if not project:
            raise Exception("no project")
        if project.status == action:
            raise Exception("current action is same ")
        if project.status == self.STOP and action == self.PAUSE:
            raise Exception("current action change is not allowed")
        spidercls = project.setting.get('spidercls', None)
        if not spidercls:
            raise Exception("project dont choose a concrete spider script")
        item = {'action': action, 'spidercls': spidercls, 'project_id': project_id}
        spidercls_queue.put(item)
        project.status = action
        db.session.commit()
        return item
