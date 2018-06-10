#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: app.py

@time: 2018/5/14 下午1:14
"""
import json
import logging
import logging.config
import traceback
from os import path

import sqlalchemy
from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy_utils import database_exists, create_database

from PyScraper.server.extensions import db, spidercls_queue
from PyScraper.server.resources.database import Databases, Database
from PyScraper.server.resources.gov_lexicon import GovLexicon, GovRule
from PyScraper.server.resources.project import Projects, Project, ProjectAction
from PyScraper.server.resources.result import Result
from PyScraper.server.resources.spider import Spiders
from PyScraper.server.resources.task import Task
from PyScraper.utils import run_in_thread

logger = logging.getLogger(__name__)


def create_app_forcontext(config='PyScraper.config.Config'):
    tmpl_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
    app = Flask("PyScraper", template_folder=tmpl_dir)
    app.config.from_object(config)
    init_db(app)

    init_app_callbacks(app)
    return app


def create_app(config='PyScraper.config.Config'):
    tmpl_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
    app = Flask("PyScraper", template_folder=tmpl_dir)
    app.config.from_object(config)
    configure_logging(app)
    configure_api(app)
    init_db(app)
    init_spider_loop(spidercls_queue)
    init_app_callbacks(app)
    
    return app


def init_db(app):
    try:
        engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        if not database_exists(engine.url):
            create_database(engine.url)
    except Exception as e:
        print(e)
    db.init_app(app)
    with app.app_context():
        from PyScraper.server.models.database import Database
        from PyScraper.server.models.project import Project
        from PyScraper.server.models.lexicon import GovLexicon
        logger.info(Database)
        logger.info(Project)
        logger.info(GovLexicon)
        db.create_all()
        logger.info('Create all tables!')


def init_spider_loop(queue):
    """单一进程内初始化spider事件循环"""
    from PyScraper.spider_loop import start_spider_loop
    run_in_thread(start_spider_loop, queue)


def init_app_callbacks(app):
    def after_clean(resp, *args, **kwargs):
        # commit db session after each request
        db.session.commit()
        return resp
    
    app.after_request(after_clean)


def configure_api(app):
    api = Api(app)
    
    @app.route("/healthz")
    def health():
        return "ready to go!\n", 200
    
    @app.route("/blank_page")
    def blank():
        return "", 200
    
    @app.route("/error_page")
    def error():
        return "", 404
    
    api.add_resource(Projects, '/projects')
    api.add_resource(Project, '/project/<int:project_id>')
    api.add_resource(ProjectAction, '/project_action/<int:project_id>')
    api.add_resource(Task, '/task/<int:project_id>')
    api.add_resource(Result, '/result/<int:project_id>')
    
    api.add_resource(Databases, '/databases')
    api.add_resource(Database, '/database/<int:database_id>')
    
    api.add_resource(Spiders, '/spiders')
    
    api.add_resource(GovLexicon, '/gov_lexicon')
    api.add_resource(GovRule, '/gov_lexicon/<int:rule_id>')

def configure_logging(app):
    config_file = '{project_path}/logger.json'
    project_path = path.join(path.dirname(path.abspath(__file__)))
    config_file = config_file.format(project_path=project_path)
    
    with open(config_file) as f:
        logging.config.dictConfig(json.load(f))
    
    # patch app logger
    for handler in logging.getLogger('').handlers:
        app.logger.addHandler(handler)


def configure_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        res = {"error": "page not found, please enter the right url"}
        return jsonify(res), 404
    
    @app.errorhandler(500)
    def handle_exception(e):
        logger.exception(e)
        exc = traceback.format_exc()
        res = {"error": exc}
        return jsonify(res), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception(e)
        exc = traceback.format_exc()
        res = {"error": exc}
        return jsonify(res), 500


if __name__ == '__main__':
    print('START PyScraper server')
    app = create_app()
    app.run()
