#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: error_correction.py

@time: 2018/5/24 下午12:45
"""
import logging
import re
from typing import List, Tuple

from scrapy.http import TextResponse

from PyScraper.server.app import create_app_forcontext
from PyScraper.server.resource_handlers.gov_lexicon_handler import GovLexiconHandler

logger = logging.getLogger(__name__)


class ErrorCorrectionExtractor:
    """
    政府网站纠错解析器
    """
    wildcard_mapping = {'?': '[\u4E00-\u9FA5]{1}', '*': '[\u4E00-\u9FA5]+?'}
    
    def __init__(self, domain: str):
        
        global_pairs = self.to_safe(self.get_global_pairs(domain=domain))
        self.compiled_pairs = self.compile_pairs(global_pairs)
        self.has_error_urls = set()
    
    def find_error(self, response: TextResponse):
        # url = response.url
        content = response.text
        error_list = []
        for compiled_pair in self.compiled_pairs:
            pattern, correct_str = compiled_pair
            complete_list = pattern.findall(content)
            complete_list = [x for x in complete_list if len(x) == len(correct_str)]  # 模糊匹配的长度保持一致
            error_list.extend([{'correct': correct_str, 'error': one} for one in complete_list if one != correct_str])
        
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
        local_pairs = pairs
        for wild_card_map_key, wild_card_map_value in self.wildcard_mapping.items():
            local_pairs = [(rule[0].replace(wild_card_map_key, wild_card_map_value), rule[1]) for rule in local_pairs]
        return local_pairs
    
    def compile_pairs(self, pairs: List[Tuple[str, str]]):
        """
        pair eg.[("关于下达温州市201([\s\S]{1})年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目")]
        """
        pairs = self.convert_pairs(pairs)
        print('规则...')
        print(str(pairs))

        return [(re.compile(pair[0]), pair[1]) for pair in pairs]
