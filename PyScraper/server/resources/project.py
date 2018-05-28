#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: project.py

@time: 2018/5/28 上午2:45
"""
from flask_restful import Resource


class Projects(Resource):
    def get(self):
        pass


class Project(Resource):
    def get(self, project_id):
        pass
    
    def put(self, project_id):
        pass
    
    def delete(self, project_id):
        pass
