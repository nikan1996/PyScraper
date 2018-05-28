#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: crawl_process.py

@time: 2018/5/28 下午1:02
"""
from scrapy.crawler import CrawlerRunner
from scrapy.resolver import CachingThreadedResolver
from scrapy.utils.log import log_scrapy_info, configure_logging
from twisted.internet import reactor


class PyScraperCrawlerProcess(CrawlerRunner):
    def __init__(self, settings=None, install_root_handler=True):
        super(PyScraperCrawlerProcess, self).__init__(settings)
        configure_logging(self.settings, install_root_handler)
        log_scrapy_info(self.settings)

    def start(self):
        reactor.installResolver(self._get_dns_resolver())
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=self.settings.getint('REACTOR_THREADPOOL_MAXSIZE'))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)  # blocking call

    def _get_dns_resolver(self):
        if self.settings.getbool('DNSCACHE_ENABLED'):
            cache_size = self.settings.getint('DNSCACHE_SIZE')
        else:
            cache_size = 0
        return CachingThreadedResolver(
            reactor=reactor,
            cache_size=cache_size,
            timeout=self.settings.getfloat('DNS_TIMEOUT')
        )

    def _graceful_stop_reactor(self):
        d = self.stop()
        d.addBoth(self._stop_reactor)
        return d

    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError:  # raised if already stopped or in shutdown stage
            pass