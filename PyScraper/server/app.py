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

from flask import Flask, jsonify
from PyScraper.server.extensions import db
from PyScraper.spider_loop import start_spider_loop
from PyScraper.utils import run_in_thread
from PyScraper.utils.multiprocessing_queue import Queue

logger = logging.getLogger(__name__)

queue = Queue()


def create_app():
    tmpl_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
    app = Flask("eigenrec", template_folder=tmpl_dir)

    configure_logging(app)
    init_db(app)
    
    init_spider_loop(queue)
    return app


def init_db(app):
    db.init_app(app)
    with app.app_context():
        logger.info('Create all tables!')
        db.create_all()


def init_spider_loop(queue):
    run_in_thread(start_spider_loop, queue)
    
    
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