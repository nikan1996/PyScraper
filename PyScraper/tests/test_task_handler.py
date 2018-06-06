#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_task_handler.py

@time: 2018/6/6 上午3:31
"""
import time

from PyScraper.server.resource_handlers.task_handler import TaskHandler
from PyScraper.tests.test_client import app, less_equal

placeholder = lambda: app  # only a placeholder to avoid pycharm import optimize


def test_task_handler(app):
    with app.app_context():
        task_handler = TaskHandler()
        project_id = 1
        url = 'https://www.test.com'
        status_code = 200
        _dict = {
            'project_id': project_id,
            'url': url,
            'status_code': status_code,
        }
        for i in range(20):
            time.sleep(0.15)
            task_handler.put_newtask(project_id=project_id, url=url, status_code=status_code)
        
        result = task_handler.get(project_id=project_id)
        assert result['count'] == 10
        assert result['total_count'] == 20
        for r in result['result']:
            assert less_equal(r, _dict)
