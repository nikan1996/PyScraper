#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project.py

@time: 2018/5/28 上午2:45
"""
from flask_restful import Resource, reqparse

from PyScraper.server.resource_handlers.project_handler import ProjectHandler, ProjectActionHandler

parser = reqparse.RequestParser()
parser.add_argument('project_name', type=str, required=True, help='project_name is required')
parser.add_argument('setting', type=dict, required=True, help='setting is required')
parser.add_argument('cron_config', type=dict, required=True, help='cron_config is required')
parser.add_argument('tag', type=str, default='', help='tag is required for string type')


class Projects(Resource):
    def get(self):
        result = ProjectHandler().get_all_projects()
        return result
    
    def put(self):
        args = parser.parse_args()
        project_name = args.project_name
        setting = args.setting
        cron_config = args.cron_config
        tag = args.tag
        if not setting.get('spidercls') and not setting.get('spider_name'):
            return {"error": "please provide spidercls or spider_name"}
        result = ProjectHandler().create_project(project_name=project_name, setting=setting, cron_config=cron_config, tag=tag)
        return result


class Project(Resource):
    def get(self, project_id):
        result = ProjectHandler().get_project(project_id)
        return result
    
    def put(self, project_id):
        args = parser.parse_args()
        project_name = args.project_name
        setting = args.setting
        cron_config = args.cron_config
        tag = args.tag
        result = ProjectHandler().update_project(project_id=project_id, project_name=project_name, setting=setting,
                                                 cron_config=cron_config, tag=tag)
        return result
    
    def delete(self, project_id):
        result = ProjectHandler().delete_project(project_id)
        return result
    

class ProjectAction(Resource):
    def put(self, project_id):
        action_parser = reqparse.RequestParser()
        action_parser.add_argument('action', type=str, required=True, help='action is required')
        args = action_parser.parse_args()
        action = args.action
        try:
            result = ProjectActionHandler().put_item_into_spider_loop(project_id, action)
            return result
        except Exception as e:
            return {"error": str(e)}, 403

