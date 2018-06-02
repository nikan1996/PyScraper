#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: spider.py

@time: 2018/6/2 上午4:27
"""
from flask_restful import Resource

from PyScraper.server.resource_handlers.spider_handler import SpiderHandler


class Spiders(Resource):
    def get(self):
        return SpiderHandler().get_all_spiders()
    
    def put(self):
        return