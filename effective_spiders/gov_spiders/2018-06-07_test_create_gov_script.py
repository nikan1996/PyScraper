#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_create_gov_script.py

@time: 2018-06-07 03:45:51
"""
from typing import List

from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse
from scrapy.link import Link
from scrapy.mail import MailSender
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import Spider

from PyScraper.extractor.blank_html import BlankHtmlExtractor
from PyScraper.extractor.error_correction import ErrorCorrectionExtractor
from PyScraper.extractor.html_link import HtmlLinkExtractor
from PyScraper.extractor.xml_link import DataProxyXmlLinkExtractor
from PyScraper.utils.mail import render_error_correction_result_mail


class test_create_gov_scriptSpider(Spider):
    name = 'test_create_gov_script'
    allowed_domains = ['wzkj.wenzhou.gov.cn']
    start_urls = ['http://wzkj.wenzhou.gov.cn/']
    rules = [
        ('关于下达温州市201[\s\S]{1}年公益性科技计划项目', '关于下达温州市2017年公益性科技计划项目'),
    ]
    htmk_link_extractor = HtmlLinkExtractor()
    error_correction_extractor = ErrorCorrectionExtractor(rules, domain='wzkj.wenzhou.gov.cn')
    blank_html_extractor = BlankHtmlExtractor()
    mailer = MailSender(smtphost='smtp.qq.com', mailfrom='859905874@qq.com', smtpport=465,
                        smtpssl=True, smtpuser='859905874@qq.com', smtppass='cgcxzdatxduybbhh')
    custom_settings = {
        # 'CONCURRENT_REQUESTS_PER_DOMAIN' : 4,
        'LOG_LEVEL': 'INFO'
        # 'DOWNLOAD_DELAY': 0.3,
    }
    
    def parse(self, response: TextResponse):
        is_blank = self.blank_html_extractor.is_blank(response)
        if is_blank:
            blank_result = {'type': 'gov', 'reason': '网页内容为空', 'url': response.url}
            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'url': response.url,
                'tablehead': ['错误原因'],
                'table_data': blank_result['reason']}
            body = render_error_correction_result_mail(**render_dict)
            self.mailer.send(to=["859905874@qq.com"], subject='(PyScraper发送）网站纠错情况', body=body, mimetype='text/html')
            yield blank_result
        
        error_correction_result = self.error_correction_extractor.find_error(response)
        if error_correction_result:
            print("error_correction_result", error_correction_result)
            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'url': response.url,
                'tablehead': ['正确词', '错误词'],
                'table_data': error_correction_result}
            body = render_error_correction_result_mail(**render_dict)
            self.mailer.send(to=["859905874@qq.com"], subject='(PyScraper发送）网站纠错情况', body=body, mimetype='text/html')
            
            yield {'type': 'gov', 'reason': '网页无法访问状态{}'.format(response.status), 'url': response.url}
        
        links: List[Link] = [lnk for lnk in self.htmk_link_extractor.extract_links(response)]
        for link in links:
            yield Request(link.url, callback=self.parse, errback=self.errorback)
        """
        获取dataproxy接口的链接
        """
        data_proxy_extractor = DataProxyXmlLinkExtractor()
        if data_proxy_extractor.has_dataproxy_link(response):
            yield data_proxy_extractor.gen_dataproxy_links()
    
    def errorback(self, failure):
        if isinstance(failure.value, HttpError):
            response = failure.value.response
            result = {'type': 'gov', 'reason': '网页无法访问状态{}'.format(response.status), 'url': response.url}
            yield result
            
            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'url': response.url,
                'tablehead': ['错误原因'],
                'table_data': result['reason']}
            body = render_error_correction_result_mail(**render_dict)
            self.mailer.send(to=["859905874@qq.com"], subject='(PyScraper发送）网站纠错情况', body=body, mimetype='text/html')
        
        print('repsonse is error in response.url:', failure)


if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
        # "LOG_FILE": "./wzkjj.log"
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(test_create_gov_scriptSpider)
    process.start()
