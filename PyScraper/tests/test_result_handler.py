#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_result_handler.py

@time: 2018/6/6 上午3:31
"""

import time

from PyScraper.server.resource_handlers.result_handler import ResultHandler
from PyScraper.tests.test_client import app, less_equal

placeholder = lambda: app  # only a placeholder to avoid pycharm import optimize


def test_result_handler(app):
    with app.app_context():
        result_handler = ResultHandler()
        project_id = 1
        result = {
            'title': '今天天气好',
            'content': '今日2018年6月6日，花正开哟'
        }
        _dict = {
            'project_id': project_id,
            'result': result,
        }
        for i in range(20):
            time.sleep(0.15)
            result_handler.put_result(project_id=project_id, result=result)
        
        result = result_handler.get(project_id=project_id)
        assert result['count'] == 10
        assert result['total_count'] == 20
        print(result['result'])
        for r in result['result']:
            assert less_equal(r, _dict)


def test_increment_result(app):
    with app.app_context():
        result_handler = ResultHandler()
        project_id = 1
        result = {
            'title': '今天天气好',
            'content': '今日2018年6月6日，花正开哟'
        }
        _dict = {
            'project_id': project_id,
            'result': result,
        }
        for i in range(20):
            time.sleep(0.15)
            result_handler.put_result(project_id=project_id, result=result, increment=True)
        
        result = result_handler.get(project_id=project_id)
        assert result['count'] == 1
        assert result['total_count'] == 1
        print(result['result'])
        for r in result['result']:
            assert less_equal(r, _dict)