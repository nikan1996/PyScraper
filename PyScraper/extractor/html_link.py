#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: html_link.py

@time: 2018/5/25 上午2:37
"""
from scrapy.link import Link
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.response import get_base_url
from sqlalchemy.util import unique_list
from w3lib.url import canonicalize_url

class HtmlLinkExtractor(LxmlLinkExtractor):
    def extract_links(self, response):
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [subdoc
                    for x in self.restrict_xpaths
                    for subdoc in response.xpath(x)]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        return unique_list(all_links, lambda link: link.url)
    
    def _process_links(self, links):
        links = super(HtmlLinkExtractor, self)._process_links(links)
        return [link for link in links if self.is_not_exclude_link(link)]
    
    def is_not_exclude_link(self, link: Link):
        exclude_prefix_list = [".doc", ".pdf",]
        for exclude_prefix in exclude_prefix_list:
            if exclude_prefix in link.url:
                return False
        return True
            
    def is_include_link(self, link: Link):
        # legal_suffix = {"html", "htm"}
        include_prefix_list = ["html", "htm"]
        for include_prefix in include_prefix_list:
            if include_prefix in link.url:
                return True
        return False
