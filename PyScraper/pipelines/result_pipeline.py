#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: result_pipeline.py

@time: 2018/6/6 下午2:44
"""
from PyScraper.server.app import create_app
from PyScraper.server.resource_handlers.result_handler import ResultHandler

import logging

logger = logging.getLogger(__name__)
class ResultPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.project_id = self.settings.get('project_id')
        self.app = create_app(spider_loop=False)
        self.result_handler = ResultHandler()
        
    def process_item(self, item, spider):
        try:
            with self.app.app_context():
                self.result_handler.put_result(project_id=self.project_id, result=dict(item))
        except Exception as e:
            logger.error(str(e))
            return item