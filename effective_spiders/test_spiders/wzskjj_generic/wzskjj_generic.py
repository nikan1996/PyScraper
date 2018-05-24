#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: wzskjj_generic.py

@time: 2018/5/24 下午12:38
"""
from scrapy import Request, Item
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.mail import MailSender
from PyScraper.extractor.error_correction import ErrorCorrectionExtractor


class WzskjjSpider(Spider):
    name = 'wzkjj'
    allowed_domains = ['wzkj.wenzhou.gov.cn']
    # start_urls = ['http://wzkj.wenzhou.gov.cn/']
    start_urls = ['http://wzkj.wenzhou.gov.cn/col/col1220139/index.html']
    rules = [
        ("关于下达温州市201[\s\S]{1}年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目")
    ]
    link_extractor = LinkExtractor()
    error_correction_extractor = ErrorCorrectionExtractor(rules)
    mailer = MailSender(smtphost='smtp.qq.com', mailfrom='859905874@qq.com', smtpport=465,
                        smtpssl=True, smtpuser='859905874@qq.com', smtppass='cgcxzdatxduybbhh')
    
    def parse(self, response):
        result = self.error_correction_extractor.find_error(response)
        print(result)
        if result:
            # self.mailer.send(to=["859905874@qq.com"], subject='Test', body='<html><body><h1>Hello</h1></body></html>', mimetype='text/html')
            # links = [lnk for lnk in self.link_extractor.extract_links(response)]
        # for link in links:
        #     yield Request(link)
            

if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
        # "LOG_FILE": "./wzkjj.log"
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(WzskjjSpider)
    process.start(stop_after_crawl=False)
