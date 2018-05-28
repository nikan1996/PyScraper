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

from queue import Queue, Empty

from PyScraper.utils.crawl_process import PyScraperCrawlerProcess

logger = logging.getLogger(__name__)
REACTOR_THREADPOOL_MAXSIZE = 20


class ScalableCrawlerProcess(PyScraperCrawlerProcess):
    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        super(ScalableCrawlerProcess, self).__init__(*args, **kwargs)
        
    def start_loop(self):
        l = task.LoopingCall(self.check_new_crawlers)
        l.start(2)  # run check_new_crawler every second
        self.start()
    
    def check_new_crawlers(self):
        try:
            spidercls = self.queue.get(timeout=1)  # Must be a spdier class that inherit scrapy.Spider
            if spidercls:
                self.crawl(crawler_or_spidercls=spidercls)
        except Empty:
            print("now is empty")
            
def start_spider_loop(queue):
    # TODO: 填入 project级配置{....}
    settings = {
        "REACTOR_THREADPOOL_MAXSIZE": 30,  # 设置reactor 线程池最大数量
        "TELNETCONSOLE_ENABLED": False,
    }
    process = ScalableCrawlerProcess(queue, settings=settings)
    #
    # # 'followall' is the name of one of the wzskjj_xxgk of the project.
    # process.crawl('followall', domain='scrapinghub.com')
    process.start_loop()  # the script will block here until the crawling is finished
    print('start')

if __name__ == '__main__':
    pass
    # start_spider_loop(queue=Queue())