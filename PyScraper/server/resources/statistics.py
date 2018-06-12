#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: statistics.py

@time: 2018/6/11 下午5:44
"""

from flask_restful import Resource

from PyScraper.server.resource_handlers.statistics_handler import StatisticsHandler


class Statistics(Resource):
    def get(self):
        result = StatisticsHandler().get_statistics()
        return result