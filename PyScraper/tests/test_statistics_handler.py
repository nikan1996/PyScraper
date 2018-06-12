#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_statistics_handler.py

@time: 2018/6/11 下午5:45
"""

import time

from PyScraper.server.resource_handlers.statistics_handler import StatisticsHandler
from PyScraper.tests.test_client import app, less_equal

placeholder = lambda: app  # only a placeholder to avoid pycharm import optimize


def test_task_handler(app):
    with app.app_context():
        statistics_handler = StatisticsHandler()
        _dict = {
            "project_num": 0,
            "running_project_num": 0,
            "all_result_num": 0
        }
        result = statistics_handler.get_statistics()
        assert less_equal(_dict, result)