#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: wzskjj_generic.py

@time: 2018/5/24 下午12:38
"""
from scrapy import Request, Item
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse, HtmlResponse
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.mail import MailSender
from scrapy.link import Link
from PyScraper.extractor.error_correction import ErrorCorrectionExtractor
from typing import List
from PyScraper.extractor.html_link import HtmlLinkExtractor
from PyScraper.extractor.xml_link import DataProxyXmlLinkExtractor
from PyScraper.utils.mail import render_mail


class WzskjjSpider(Spider):
    name = 'wzkjj'
    allowed_domains = ['wzkj.wenzhou.gov.cn']
    start_urls = ['http://wzkj.wenzhou.gov.cn/']
    rules = [
        ("关于下达温州市201[\s\S]{1}年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目")
    ]
    htmk_link_extractor = HtmlLinkExtractor()
    error_correction_extractor = ErrorCorrectionExtractor(rules)
    mailer = MailSender(smtphost='smtp.qq.com', mailfrom='859905874@qq.com', smtpport=465,
                        smtpssl=True, smtpuser='859905874@qq.com', smtppass='cgcxzdatxduybbhh')
    custom_settings = {
    'CONCURRENT_REQUESTS_PER_DOMAIN' : 4,
    'LOG_LEVEL': 'INFO'
        # 'DOWNLOAD_DELAY': 0.3,
    }
    
    def parse(self, response: TextResponse):
        result = self.error_correction_extractor.find_error(response)
        if result:
            print("error_correction_result", result)
            table_data = [{'correct': r['correct'], 'error': r['error'], 'url': response.url} for r in result]
            render_dict = {
                'title': '（PyScraper发送）错误网站',
                'table_head': ['正确词', '错误词', '网站地址'],
                'table_data': table_data}
            body = render_mail(render_dict['title'], render_dict['table_head'], render_dict['table_data'])
            self.mailer.send(to=["859905874@qq.com"], subject='PyScraper发送）网站纠错情况', body=body, mimetype='text/html')
        links: List[Link] = [lnk for lnk in self.htmk_link_extractor.extract_links(response)]
        for link in links:
            # print(link)
            yield Request(link.url, callback=self.parse, errback=self.errorback)
        """
        获取dataproxy接口的链接
        """
        # d = Deffer
        data_proxy_extractor = DataProxyXmlLinkExtractor()
        if data_proxy_extractor.has_dataproxy_link(response):
            yield data_proxy_extractor.gen_dataproxy_links()
            # for data_proxy_link in data_proxy_links:
                # yield Request(data_proxy_link, callback=self.yield_dataproxy_link, meta={'data_proxy_extractor': data_proxy_extractor})
            
    def errorback(self, failure):
        print('resonse is error in response.url:', failure)

    # def yield_dataproxy_link(self, response):
    #     """判断政府网站是否包括dataproxy接口的探测与解析"""
    #     data_proxy_extractor: DataProxyXmlLinkExtractor = response.meta.get('data_proxy_extractor')
    #     record_urls = data_proxy_extractor.dataproxy_xml_extract(response.text)
    #     for url in record_urls:
    #         yield Request(url, callback=self.parse)
    
    
if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
        # "LOG_FILE": "./wzkjj.log"
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(WzskjjSpider)
    process.start()
