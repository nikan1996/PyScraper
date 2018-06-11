#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: error_correction.py

@time: 2018/5/24 下午12:45
"""
import re
from typing import List, Pattern, Tuple

from scrapy.http import TextResponse

from PyScraper.server.app import create_app_forcontext
from PyScraper.server.resource_handlers.gov_lexicon_handler import GovLexiconHandler


class ErrorCorrectionExtractor:
    """
    政府网站纠错解析器
    """
    wildcard_mapping = {'*': '[\s\S]{1}'}
    
    def __init__(self, pairs: List[(Tuple or List)[str, str]], domain: str):
        pairs = self.to_safe(pairs)
        
        global_pairs = self.to_safe(self.get_global_pairs(domain=domain))
        self.compiled_pairs: List[Tuple[Pattern, str]] = self.compile_pairs(pairs + global_pairs)
        
        self.has_error_urls = set()
    
    def find_error(self, response: TextResponse):
        # url = response.url
        content = response.text
        error_list = []
        for compiled_pair in self.compiled_pairs:
            pattern, correct_str = compiled_pair
            complete_list = pattern.findall(content)
            error_list = [{'correct': correct_str, 'error': one} for one in complete_list if one != correct_str]
        
        if error_list and response.url not in self.has_error_urls:
            self.has_error_urls.add(response.url)
            return error_list
    
    @staticmethod
    def to_safe(pairs: List[Tuple[str, str]]):
        return [pair for pair in pairs if all(pair)]
    
    @staticmethod
    def get_global_pairs(domain: str):
        app = create_app_forcontext()
        with app.app_context():
            return GovLexiconHandler().get_all_rules_by_domain(domain)
    
    def convert_pairs(self, pairs: List[Tuple[str, str]]):
        return [(rule[0].replace('*', self.wildcard_mapping['*']), rule[1]) for rule in pairs]
    
    def compile_pairs(self, pairs: List[Tuple[str, str]]):
        pairs = self.convert_pairs(pairs)
        """
        pair eg.[("关于下达温州市201([\s\S]{1})年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目")]
        :return:
        """
        return [(re.compile(pair[0]), pair[1]) for pair in pairs]
