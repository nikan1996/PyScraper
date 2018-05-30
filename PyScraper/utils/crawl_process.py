#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: crawl_process.py

@time: 2018/5/28 下午1:02
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import log_scrapy_info, configure_logging
from twisted.internet import reactor


class PyScraperCrawlerProcess(CrawlerProcess):
    def __init__(self, in_thread, settings=None, install_root_handler=True):
        # call grandparent init method
        # avoid calling CrawlerProcess init method which install shutdown_handlers
        if in_thread:
            super(CrawlerProcess, self).__init__(settings)
            configure_logging(self.settings, install_root_handler)
            log_scrapy_info(self.settings)
        else:
            super(PyScraperCrawlerProcess, self).__init__(settings, install_root_handler)

    def start(self, stop_after_crawl=False):
        super(PyScraperCrawlerProcess, self).start(stop_after_crawl=stop_after_crawl)