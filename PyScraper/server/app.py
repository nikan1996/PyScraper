#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: app.py

@time: 2018/5/14 下午1:14
"""
import json
import traceback
from os import path
import os
from flask import Flask, jsonify
import logging

logger = logging.getLogger(__name__)

def create_app():
    tmpl_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
    app = Flask("eigenrec", template_folder=tmpl_dir)

    configure_logging(app)
    
    return app

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