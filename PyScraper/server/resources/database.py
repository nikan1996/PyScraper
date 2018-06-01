#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: database_handler.py

@time: 2018/5/14 下午1:59
"""
import json

from flask_restful import Resource, reqparse
from flask import request
from PyScraper.server.resource_handlers.database_handler import DatabaseHandler

parser = reqparse.RequestParser()
parser.add_argument('database_name', type=str, required=True, help='database_name is required')
parser.add_argument('config', type=dict, required=True, help='config is required')


class Databases(Resource):
    def get(self):
        result = DatabaseHandler().get_all_databases()
        return result
    
    def put(self):
        print(1)
        # create a new project
        args = parser.parse_args()
        database_name = args.database_name
        config = args.config
        handler = DatabaseHandler()
        error = handler.check_database_available(config)
        if not error:
            result = handler.create_database(database_name, config)
            return result
        else:
            return {"error": error}, 403


class Database(Resource):
    def get(self, database_id):
        result = DatabaseHandler().get_database(database_id)
        return result
    
    def put(self, database_id):
        args = parser.parse_args()
        database_name = args.database_name
        config = args.config
        result = DatabaseHandler().update_database(database_id=database_id, database_name=database_name, config=config)
        return result
    
    def delete(self, database_id):
        result = DatabaseHandler().delete_database(database_id)
        return result
