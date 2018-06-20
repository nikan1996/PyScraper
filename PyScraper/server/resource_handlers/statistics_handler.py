#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: statistics_handler.py

@time: 2018/6/11 下午2:35
"""

from PyScraper.server.models.project import Project
from PyScraper.server.models.result import Result
from PyScraper.server.models.task import Task


class StatisticsHandler:
    def get_statistics(self):
        project_num = Project.query.filter_by(is_deleted=0).count()
        running_project_num = Project.query.filter_by(status="running", is_deleted=0).count()
        all_result_num = Result.query.count()
        all_task_num = Task.query.count()
        return {
            "project_num": project_num,
            "running_project_num": running_project_num,
            "all_result_num": all_result_num,
            "all_task_num": all_task_num,
        }
