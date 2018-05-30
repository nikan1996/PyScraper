#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: spider_loop.py

@time: 28/02/2018 12:19 PM
"""
import logging
from queue import Empty

from twisted.internet import task
from scrapy.crawler import Crawler
from scrapy.core.engine import ExecutionEngine
from PyScraper.utils.crawl_process import PyScraperCrawlerProcess

logger = logging.getLogger(__name__)


class ScalableCrawlerProcess(PyScraperCrawlerProcess):
    def __init__(self, queue, in_thread=True, *args, **kwargs):
        self.queue = queue
        self.spider_cls_bind_crawlers = {}
        super(ScalableCrawlerProcess, self).__init__(in_thread, *args, **kwargs)
    
    def start_loop(self):
        l = task.LoopingCall(self.check_new_crawlers)
        l.start(2)  # run check_new_crawler every second
        self.start()
    
    def check_new_crawlers(self):
        try:
            item = self.queue.get(timeout=1)  # Must be a spdier class that inherit scrapy.Spider
            action = item.get('action')
            spidercls = item.get('spidercls')
            if not spidercls:
                logger.error("no spidercls in queue item")
                raise Exception("no spidercls in queue item")
            status = self.spider_cls_bind_crawlers.get(str(spidercls), {}).get('status')
            if action == 'start':
                if not status:
                    self.start_a_crawler(spidercls=spidercls)
                if status == 'pause':
                    self.unpause_a_crawler(spidercls=spidercls)
            if action == 'stop':
                self.stop_a_crawler(spidercls=spidercls)
            if action == 'pause':
                self.pause_a_crawler(spidercls=spidercls)
        except Empty:
            print("now is empty")
    
    def pause_a_crawler(self, *, spidercls):
        crawler: Crawler = self.spider_cls_bind_crawlers[str(spidercls)].get('crawler')
        engine: ExecutionEngine = crawler.engine
        engine.pause()
        self.spider_cls_bind_crawlers[str(spidercls)]['status'] = 'pause'
        print('pause {}'.format(str(spidercls)))
    
    def unpause_a_crawler(self, *, spidercls):
        crawler: Crawler = self.spider_cls_bind_crawlers[str(spidercls)].get('crawler')
        engine: ExecutionEngine = crawler.engine
        engine.unpause()
        self.spider_cls_bind_crawlers[str(spidercls)]['status'] = 'start'

        print('unpause {}'.format(str(spidercls)))
    
    def start_a_crawler(self, *, spidercls):
        self.crawl(crawler_or_spidercls=spidercls)
    
    def stop_a_crawler(self, *, spidercls):
        crawler: Crawler = self.spider_cls_bind_crawlers[str(spidercls)].get('crawler')
        self.spider_cls_bind_crawlers[str(spidercls)]['status'] = 'stop'

        crawler.stop()
    
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        crawler = self.create_crawler(crawler_or_spidercls)
        self.spider_cls_bind_crawlers[str(crawler_or_spidercls)] = {'crawler': crawler, 'status': 'start'}
        return self._crawl(crawler, *args, **kwargs)


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
    # start_spider_loop(spider_cls_queue=Queue())
