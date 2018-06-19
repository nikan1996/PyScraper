#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: wzskjj.py

@time: 2018-06-19 10:33:14
"""
from typing import List

import re
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


class wzskjjSpider(Spider):
    name = 'wzskjj'
    allowed_domains = ['wzkj.wenzhou.gov.cn']
    start_urls = ['http://wzkj.wenzhou.gov.cn/col/col1220133/index.html###']
    htmk_link_extractor = HtmlLinkExtractor()
    error_correction_extractor = ErrorCorrectionExtractor(domain='wzkj.wenzhou.gov.cn')
    blank_html_extractor = BlankHtmlExtractor()
    custom_settings = {
    # 'CONCURRENT_REQUESTS_PER_DOMAIN' : 4,
    'LOG_LEVEL': 'DEBUG',
    'DOWNLOAD_MAXSIZE': 273741,
    # 'DOWNLOAD_DELAY': 0.3,
    }

    def parse(self, response: TextResponse):
        request_url = response.meta.get("url")
        previous_url = response.meta.get("previous_url")
        previous_content = response.meta.get("previous_content")
        response_is_blank = self.blank_html_extractor.is_blank(response)
        for sufix in ['.html', '.htm', '.jsp', '.asp']:
            if sufix in response.url:
                if response_is_blank:
                    blank_result = {'type': 'error_link', 'reason': '网页内容为空', 'url': request_url or response.url, 'content': response.text,  "previous_url": previous_url, 'status': 200, "previous_content": previous_content}
                    yield blank_result


        error_correction_result = self.error_correction_extractor.find_error(response)
        if error_correction_result:
            print("error_correction_result", error_correction_result)

            message = "\n".join(["正确词：{} 错误词： {}".format(error['correct'], error['error']) for error in error_correction_result])
            yield {'type': 'error_word', 'reason': '网页中有错误词:\n' + message, 'url': request_url or response.url, 'content': response.text, 'error': error_correction_result}

        """
        获取urls[i]='/art/2018/3/7/art_1220133_15759129.html'形式的链接
        """
        urls = [response.urljoin(url) for url in re.findall("urls\[i\]='(.+?)'", response.text)]
        for url in urls:
            yield Request(url, callback=self.parse, errback=self.errorback,
                          meta={"url": url, "previous_url": response.url, "previous_content": response.text})

        # links: List[Link] = [lnk for lnk in self.htmk_link_extractor.extract_links(response)]
        # for link in links:
        #     yield Request(link.url, callback=self.parse, errback=self.errorback,
        #                     meta={"url": link.url, "previous_url": response.url, "previous_content": response.text})
        """
        获取dataproxy接口的链接
        """
        # data_proxy_extractor = DataProxyXmlLinkExtractor()
        # if data_proxy_extractor.has_dataproxy_link(response):
        #     yield data_proxy_extractor.gen_dataproxy_links()

    def errorback(self, failure):
        if isinstance(failure.value, HttpError):
            response = failure.value.response
            request_url = response.meta.get("url")
            previous_url = response.meta.get("previous_url")
            previous_content = response.meta.get("previous_content")
            result = {'type': 'error_link', 'reason': '错误链接{}'.format(response.status), 'status': response.status, 'url': request_url or response.url, 'content': None,  "previous_url": previous_url,  "previous_content": previous_content}
            yield result


        print('response is error in response.url:', failure)


if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
        # "LOG_FILE": "./wzkjj.log"
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(wzskjjSpider)
    process.start()