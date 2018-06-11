#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: a2018611wzskjj.py

@time: 2018-06-11 00:20:05
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


class a2018611wzskjjSpider(Spider):
    name = 'a2018611wzskjj'
    allowed_domains = ['wzkj.wenzhou.gov.cn']
    start_urls = ['http://wzkj.wenzhou.gov.cn/']
    rules = [
        ['温州市201*', '温州市2017']
    ]
    htmk_link_extractor = HtmlLinkExtractor()
    error_correction_extractor = ErrorCorrectionExtractor(rules, domain='wzkj.wenzhou.gov.cn')
    blank_html_extractor = BlankHtmlExtractor()
    mailer = MailSender(smtphost='smtp.qq.com', mailfrom='859905874@qq.com', smtpport=465,
                        smtpssl=True, smtpuser='859905874@qq.com', smtppass='cgcxzdatxduybbhh')
    custom_settings = {
        # 'CONCURRENT_REQUESTS_PER_DOMAIN' : ,
        'LOG_LEVEL': 'DEBUG'
        # 'DOWNLOAD_DELAY': 0.3,
    }
    
    def parse(self, response: TextResponse):
        request_url = response.meta.get("url")
        first_url = response.meta.get("first_url")
        response_is_blank = self.blank_html_extractor.is_blank(response)
        if response_is_blank:
            blank_result = {'type': 'gov', 'reason': '网页内容为空', 'url': request_url or response.url, 'first_url': first_url}
            yield blank_result
            
            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'url': request_url or response.url,
                'table_head': ['错误原因'],
                'table_data': blank_result['reason']}
            body = render_error_correction_result_mail(**render_dict)
            self.mailer.send(to=["859905874@qq.com"], subject='(PyScraper发送）网站纠错情况', body=body, mimetype='text/html')

        error_correction_result = self.error_correction_extractor.find_error(response)
        if error_correction_result:
            print("error_correction_result", error_correction_result)

            message = "\n".join(
                ["正确词：{} 错误词： {}".format(error['correct'], error['error']) for error in error_correction_result])
            yield {'type': 'gov', 'reason': '网页中有错误词:\n' + message, 'url': request_url or response.url}

            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'url': request_url or response.url,
                'table_head': ['正确词', '错误词'],
                'table_data': error_correction_result}
            body = render_error_correction_result_mail(**render_dict)
            self.mailer.send(to=["859905874@qq.com"], subject='(PyScraper发送）网站纠错情况', body=body, mimetype='text/html')

        links: List[Link] = [lnk for lnk in self.htmk_link_extractor.extract_links(response)]
        for link in links:
            yield Request(link.url, callback=self.parse, errback=self.errorback,
                          meta={"url": link.url, "first_url": request_url or response.url})
        """
        获取dataproxy接口的链接
        """
        data_proxy_extractor = DataProxyXmlLinkExtractor()
        if data_proxy_extractor.has_dataproxy_link(response):
            yield data_proxy_extractor.gen_dataproxy_links()
    
    def errorback(self, failure):
        
        if isinstance(failure.value, HttpError):
            response = failure.value.response
            request_url = response.meta.get("url")
            first_url = response.meta.get("first_url")
            
            result = {'type': 'gov', 'reason': '网页无法访问状态{}'.format(response.status), 'url': request_url or response.url,
                      'first_url': first_url}
            yield result
            
            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'url': first_url or response.url,
                'table_head': ['错误原因'],
                'table_data': result['reason']}
            body = render_error_correction_result_mail(**render_dict)
            # self.mailer.send(to=["859905874@qq.com"], subject='(PyScraper发送）网站纠错情况', body=body, mimetype='text/html')
        
        print('response is error in response.url:', failure)


if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
        # "LOG_FILE": "./wzkjj.log"
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(a2018611wzskjjSpider)
    process.start()
