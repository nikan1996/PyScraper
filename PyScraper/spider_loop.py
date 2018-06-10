#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: spider_loop.py

@time: 28/02/2018 12:19 PM
"""
import logging
from queue import Empty

from scrapy.core.engine import ExecutionEngine
from scrapy.crawler import Crawler
from twisted.internet import task

from PyScraper.server.app import create_app_forcontext
from PyScraper.server.resource_handlers.project_handler import ProjectHandler
from PyScraper.utils import import_class
from PyScraper.utils.crawl_process import PyScraperCrawlerProcess

logger = logging.getLogger(__name__)


class ScalableCrawlerProcess(PyScraperCrawlerProcess):
    def __init__(self, queue, in_thread=True, *args, **kwargs):
        self.app = create_app_forcontext()
        self.queue = queue
        self.spiderclses = {}  # {'cls1':{'spidercls':'cls1','crawler': crawler, 'status': 'start', 'project_id': 1}}
        super(ScalableCrawlerProcess, self).__init__(in_thread, *args, **kwargs)
        
        self.t = None
    
    def start_loop(self):
        self.t = task.LoopingCall(self.check_new_crawlers)
        self.t.start(0.5).addErrback(self.restart_loop)  # run check_new_crawler every second
        self.start()
    
    def restart_loop(self, failure):
        logger.error(str(failure))
        self.t.start(0.5).addErrback(self.restart_loop)
    
    def check_new_crawlers(self):
        try:
            item = self.queue.get(timeout=1)
            action = item.get('action')
            spidercls = item.get('spidercls')
            project_id = item.get('project_id')
            
            if not spidercls:
                logger.error("no spidercls in queue item")
                raise Exception("no spidercls in queue item")
            
            spidercls_info = self.get_spidercls_info(spidercls)
            status = spidercls_info.get('status')
            if action == status:
                raise Exception("dont pass action which is same as current status")
            
            if action == 'start':
                if status == 'pause':
                    self.unpause_a_crawler(spidercls_info=spidercls_info)
                else:
                    self.start_a_crawler(project_id=project_id, spidercls=spidercls)
            elif action == 'stop':
                if status == 'pause' or 'start':
                    self.stop_a_crawler(spidercls_info=spidercls_info)
            elif action == 'pause':
                if status == 'start':
                    self.pause_a_crawler(spidercls_info=spidercls_info)
                if status == 'stop':
                    raise Exception("pause is not allowed when crawler is stopped")
            else:
                raise Exception("dont pass unknown action")
            
            # when action is stop, cralwer has a callback to update status after stopped.
            if action != 'stop':
                self.update_spidercls_status(spidercls, action)
        
        except Empty:
            pass
            # logger.info("now spidercls queue is empty")
    
    def pause_a_crawler(self, *, spidercls_info: dict):
        crawler: Crawler = spidercls_info.get('crawler')
        engine: ExecutionEngine = crawler.engine
        engine.pause()
        print('pause {}'.format(spidercls_info))
    
    def unpause_a_crawler(self, *, spidercls_info: dict):
        crawler: Crawler = spidercls_info.get('crawler')
        engine: ExecutionEngine = crawler.engine
        engine.unpause()
        print('unpause {}'.format(spidercls_info))
    
    def start_a_crawler(self, *, project_id: int, spidercls: str):
        self.crawl(crawler_or_spidercls=import_class(spidercls), spidercls=spidercls, project_id=project_id)
    
    def stop_a_crawler(self, *, spidercls_info: dict):
        crawler: Crawler = spidercls_info.get('crawler')
        crawler.stop()
    
    def _crawl(self, crawler, *args, spidercls=None, **kwargs):
        self.crawlers.add(crawler)
        d = crawler.crawl(*args, **kwargs)
        self._active.add(d)
        
        def _done(result):
            self.crawlers.discard(crawler)
            self._active.discard(d)
            self.crawler_stop(spidercls)
            return result
        
        return d.addBoth(_done)
    
    def crawl(self, crawler_or_spidercls, spidercls=None, project_id=None, *args, **kwargs):
        self.spiderclses[spidercls] = {'crawler': None,
                                       'status': 'start', 'project_id': project_id}
        crawler = self.create_crawler2(spidercls_cls=crawler_or_spidercls, spidercls_str=spidercls)
        self.spiderclses[spidercls]['crawler'] = crawler
        logger.info('start crawl {}'.format(self.spiderclses[spidercls]))
        return self._crawl(crawler, *args, crawler_or_spidercls=crawler_or_spidercls, spidercls=spidercls, **kwargs)
    
    def create_crawler2(self, spidercls_cls, spidercls_str):
        cls_settings = self.settings.copy()
        spidercls_info = self.get_spidercls_info(spidercls_str)
        extra_info = {'project_id': spidercls_info.get('project_id')}
        cls_settings.setdict(extra_info)
        logger.info(cls_settings)
        return Crawler(spidercls_cls, cls_settings)
    
    def crawler_stop(self, spidercls):
        self.update_spidercls_status(spidercls, 'stop')
        logger.info('crawler {} stop'.format(spidercls))
    
    def get_spidercls_info(self, spidercls: str):
        return self.spiderclses.get(spidercls, {})
    
    def update_spidercls_status(self, spidercls: str, status: str):
        spidercls_info = self.get_spidercls_info(spidercls)
        project_id = spidercls_info['project_id']
        self._update_project_status(project_id=project_id, status=status)
        spidercls_info['status'] = status
    
    def _update_project_status(self, project_id, status):
        print('update project status...')
        print('project{} is {}'.format(project_id, status))
        with self.app.app_context():
            ProjectHandler().update_project_status(project_id, status)


def start_spider_loop(queue):
    # TODO: 填入 project级配置{....}
    settings = {
        'REACTOR_THREADPOOL_MAXSIZE': 30,  # 设置reactor 线程池最大数量
        'TELNETCONSOLE_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'PyScraper.middlewares.downloadmiddlewares.put_task_middleware.TaskMiddleware': 999,
        },
        'ITEM_PIPELINES': {
            'PyScraper.pipelines.result_pipeline.ResultPipeline': 999
        }
    }
    process = ScalableCrawlerProcess(queue, settings=settings)
    #
    # # 'followall' is the name of one of the wzskjj_xxgk of the project.
    # process.crawl('followall', domain='scrapinghub.com')
    process.start_loop()  # the script will block here until the crawling is finished
    print('start')


if __name__ == '__main__':
    pass
    # start_spider_loop(spidercls_queue=Queue())
