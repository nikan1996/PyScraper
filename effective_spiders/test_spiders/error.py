#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: error.py

@time: 2018/6/8 下午6:15
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse


class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ExampleErrorSpider(scrapy.Spider):
    name = 'example_error'
    allowed_domains = ['example.com']
    
    def start_requests(self):
        start_urls = ['http://www.example.com/error']
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response: TextResponse):
        yield {'test': 'haha'}


if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(ExampleErrorSpider)
    process.start()
