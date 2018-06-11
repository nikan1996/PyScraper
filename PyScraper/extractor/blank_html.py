#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: blank_html.py

@time: 2018/6/8 下午4:32
"""
from scrapy.http import TextResponse, Response
from bs4 import BeautifulSoup


class BlankHtmlExtractor:
    def is_blank(self, response: TextResponse or str):
        if isinstance(response, str):
            content = response
        elif isinstance(response, TextResponse):
            content = response.text
        else:
            raise Exception("response need be string or TextResponse")
        soup = BeautifulSoup(content, 'lxml')
        if soup.body and soup.body.text.strip():
            return False
        return True