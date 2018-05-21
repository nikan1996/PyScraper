#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: spider_loop.py

@time: 28/02/2018 12:19 PM
"""
import logging

from scrapy.utils.project import get_project_settings
from twisted.internet import task
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import click

from PyScraper.spiders.wzskjj_xxgk.wzskjj_xxgk.spiders.example import Wzskjj_xxgkSpider
from queue import Queue
logger = logging.getLogger(__name__)
REACTOR_THREADPOOL_MAXSIZE = 20


class ScalableCrawlerProcess(CrawlerProcess):
    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        super(ScalableCrawlerProcess, self).__init__(*args, **kwargs)
        
    def start_loop(self):
        REACTOR_THREADPOOL_MAXSIZE = 20  # 设置reactore 线程池最大数量
        l = task.LoopingCall(self.check_new_crawlers)
        l.start(20)  # run check_new_crawler every second
        self.start(stop_after_crawl=False)
    
    def check_new_crawlers(self):
        spidercls = self.queue.get(timeout=1)  # Must be a spdier class that inherit scrapy.Spider
        if 1:
            self.crawl(crawler_or_spidercls=spidercls)
            
            
def start_spider_loop(queue):
    process = ScalableCrawlerProcess(queue)
    #
    # # 'followall' is the name of one of the wzskjj_xxgk of the project.
    # process.crawl('followall', domain='scrapinghub.com')
    process.start_loop()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    start_spider_loop(queue=Queue())