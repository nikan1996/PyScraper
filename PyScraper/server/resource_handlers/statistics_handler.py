#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: statistics_handler.py

@time: 2018/6/11 下午2:35
"""


from PyScraper.server.models.project import Project
from PyScraper.server.models.result import Result

class StatisticsHandler:
    def get_statistics(self):
        project_num = Project.query.
    