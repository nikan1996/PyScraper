#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: example.py

@time: 2018/5/30 下午4:22
"""

import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse
from twisted.internet import reactor
from PyScraper.utils.twisted_utils import aiosleep
from twisted.internet.defer import inlineCallbacks


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    
    def start_requests(self):
        start_urls = ['http://example.com/']
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response: TextResponse):
        yield {'test': 'haha'}


class BlockExampleSpider(ExampleSpider):
    name = 'block_example'
    custom_settings = {
        # 'DOWNLOAD_DELAY': 2,
        # 'CONCURRENT_REQUESTS': 1
    }
    
    def parse(self, response: TextResponse):
        yield {'test': 'haha'}
        print("example will hang 60 second ")
        for i in range(30):
            yield scrapy.Request("http://example.com/", callback=self.parse, dont_filter=True)

        print("example was stopped now")


class BlockExampleSpider2(BlockExampleSpider):
    name = 'block_example2'


if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(ExampleSpider)
    process.start()
