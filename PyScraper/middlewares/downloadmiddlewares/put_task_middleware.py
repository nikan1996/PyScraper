#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: put_task_middleware.py

@time: 2018/6/6 下午3:52
"""
from scrapy.exceptions import IgnoreRequest
from scrapy.http import TextResponse

from PyScraper.server.app import create_app_forcontext
from PyScraper.server.resource_handlers.task_handler import TaskHandler
import logging

logger = logging.getLogger(__name__)

class TaskMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        self.project_id = self.settings.get('project_id')
        self.app = create_app_forcontext()
        self.task_handler = TaskHandler()

    def process_response(self, request, response:TextResponse, spider):
        url = request.url
        status = response.status
        content= response.text
        try:
            with self.app.app_context():
                self.task_handler.put_newtask(project_id=self.project_id, content=content, url=url, status_code=status)
        except Exception as e:
            logger.error(str(e))
        return response
    
    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            return
        
        url = request.url
        with self.app.app_context():
            self.task_handler.put_newtask(project_id=self.project_id, url=url, status_code=403, reason=str(exception))