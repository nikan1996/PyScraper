#!/usr/bin/env python
# encoding: utf-8
"""
模块支持政府网站（已测试）：
{
'温州市科学技术局': "http://wzkj.wenzhou.gov.cn/",
'舟山市科学技术局': "http://zskjj.zhoushan.gov.cn/",

}
@author:nikan

@file: xml_link.py

@time: 2018/5/24 下午9:40
"""
import re
from urllib.parse import urljoin
from xml.etree import ElementTree

from scrapy import Request
from scrapy.http import HtmlResponse


class DataProxyXmlLinkExtractor:
    def __init__(self):
        self.url = None  # 网站url
        search_pattern = "['\"](/module/jpage/.*?dataproxy\.jsp\?page=1.+?)['\"]"
        self.search_compile = re.compile(search_pattern)
        self.dataproxy_first_page_url = None
        
        self.total_record = None
        self.total_page = None
        self.record_urls = None
    
    def has_dataproxy_link(self, response):
        text = response.text
        self.url = response.url
        search = self.search_compile.search(text)
        if search:
            url = search.group(1)
            abstract_url = urljoin(self.url, url)
            self.dataproxy_first_page_url = abstract_url
            return True
        return False
    
    def yield_dataproxy_first_page_url(self):
        """
        :return:
        """
        yield Request(self.dataproxy_first_page_url)
    
    def gen_dataproxy_links(self, callback=None):
        """
        请在爬虫中调用该函数，
        :param callback:
        :return:
        """
        if not self.dataproxy_first_page_url:
            raise ValueError("请先获取dataproxy首页url")
        r = Request(self.dataproxy_first_page_url, callback=self.yield_all_dataproxy_links)
        return r
    
    def yield_all_dataproxy_links(self, response: HtmlResponse):
        self.dataproxy_xml_extract(response.text, first_page=True)
        for num in range(1, self.total_page + 1):
            later_url = self.dataproxy_first_page_url.replace("page=1", "page={num}".format(num=num))
            yield Request(later_url, callback=self.yield_record_link,  meta={"url": later_url, "previous_url": response.url})
    
    def yield_record_link(self, response):
        """判断政府网站是否包括dataproxy接口的探测与解析"""
        record_urls = self.dataproxy_xml_extract(response.text)
        for url in record_urls:
            yield Request(url, meta={"url": url, "previous_url": response.url})
            
    def get_recordset_href(self, record_set: [ElementTree.Element]):
        """
        return an abstract url in record
        """
        record_urls = []
        for record in record_set:
            find = re.search("href=['\"](.+?)['\"]", record.text)
            if find:
                relative_url = find.group(1)
                abstract_url = urljoin(self.url, relative_url)
                record_urls.append(abstract_url)
        return record_urls
    
    def dataproxy_xml_extract(self, xml, first_page=False):
        """
        
        :param xml:
        :param first_page:
        :return: record_urls
        """
        # try:
        root = ElementTree.fromstring(xml)
        
        children = list(root)
        if first_page:
            self.total_record = int(list(root.iter('totalrecord'))[0].text)
            self.total_page = int(list(root.iter('totalpage'))[0].text)
        record_set = list(root.iter('recordset'))[0]
        record_urls = self.get_recordset_href(record_set)
        return record_urls
        # except Exception as e:
        #     print(e)
