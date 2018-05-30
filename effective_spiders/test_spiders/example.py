#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: example.py

@time: 2018/5/30 下午4:22
"""

import re
import scrapy
import time
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse


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
        pass

class BlockExampleSpider(ExampleSpider):
    def parse(self, response: TextResponse):
        print("example will hang 60 second")
        time.sleep(60)
        print("example was stopped now")
        
        
if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(ExampleSpider)
    process.start()