#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: database_handler.py

@time: 2018/5/28 下午2:12
"""
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.database import Database


class DatabaseHandler:
    def get_all_databases(self):
        all = Database.query.all()
        return convert_query_result2dict(all)
    
    def get_database(self, database_id):
        return convert_query_result2dict(Database.query.filter_by(database_id=database_id).first())

    def delete_project(self, database_id):
        return database_id

    def update_project(self, database_id, ):
        database = Database.query.filter_by(database_id=database_id).first()
        return convert_query_result2dict(database)
