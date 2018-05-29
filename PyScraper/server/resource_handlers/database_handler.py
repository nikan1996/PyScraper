#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: database_handler.py

@time: 2018/5/28 下午2:12
"""
import pymysql

from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.database import Database
import copy


class DatabaseHandler:
    def get_all_databases(self):
        all = Database.query.filter_by(is_deleted=0).all()
        return convert_query_result2dict(all)
    
    def check_database_available(self, config):
        try:
            config = config.copy()
            config['port'] = int(config['port'])
            connection = pymysql.connect(**config)
            connection.close()
        except Exception as e:
            return e
        return 0
    
    def create_database(self, database_name, config):
        new_db = Database(database_name=database_name, config=config)
        db.session.add(new_db)
        db.session.commit()
        result = convert_query_result2dict(new_db)
        return result
    
    def get_database(self, database_id):
        return convert_query_result2dict(Database.query.filter_by(database_id=database_id, is_deleted=0).first())
    
    def delete_database(self, database_id):
        database = Database.query.filter_by(database_id=database_id).first()
        if database:
            database.is_deleted = 1
        db.session.commit()
        print(database.is_deleted)
        print('is deleted')
        print(convert_query_result2dict(database))
        return convert_query_result2dict(database)
    
    def update_database(self, *, database_id, database_name, config):
        database = Database.query.filter_by(database_id=database_id, is_deleted=0).first()
        if not database:
            return None
        database.database_name = database_name
        database.config = config
        db.session.commit()
        return convert_query_result2dict(database)
