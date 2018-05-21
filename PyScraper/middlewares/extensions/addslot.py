# encoding: utf-8

import logging

from scrapy import signals
from scrapy.core.downloader import Slot
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class AddSlot(object):
    def __init__(self, crawler):
        """自定义SLOT"""
        self.crawler = crawler
        self.settings = crawler.settings        
        self.downloader_slots = None
        self.randomize_delay = self.settings.getbool('RANDOMIZE_DOWNLOAD_DELAY')
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
    
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ADDSLOT_ENABLED'):
            raise NotConfigured
        return cls(crawler)
    
    def spider_opened(self, spider):
        self.downloader_slots = self.crawler.engine.downloader.slots
        if self.settings.get('SLOTS'):
            for slot_name, slot_config in self.settings.get('SLOTS').items():
                concurrency = slot_config.get('concurrency')
                delay = slot_config.get('delay')
                randomize_delay = slot_config.get('randomize_delay') or self.randomize_delay
                if concurrency is None:
                    str = 'slot {name} should have concurrency in config'.format(name=slot_name)
                    raise Exception(str)
                if delay is None:
                    str = 'slot {name} should have delay in config'.format(name=slot_name)
                    raise Exception(str)
                self.downloader_slots[slot_name] = Slot(concurrency, delay, randomize_delay=randomize_delay)
                logger.info('ADDED YOUR SLOTS `{NAME}`'.format(NAME=slot_name))
