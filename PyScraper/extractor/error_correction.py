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


class ErrorCorrectionExtractor:
    """
    政府网站纠错解析器
    """
    
    def __init__(self, pairs: List[Tuple[str, str]]):
        pairs = self.to_safe(pairs)
        self.compiled_pairs: List[Tuple[Pattern, str]] = self.compile_pairs(pairs)
    
    def find_error(self, response: TextResponse):
        # url = response.url
        content = response.text
        error_list = []
        for compiled_pair in self.compiled_pairs:
            pattern, correct_str = compiled_pair
            complete_list = pattern.findall(content)
            error_list = [one for one in complete_list if one != correct_str]
        return error_list


    @staticmethod
    def to_safe(pairs: List[Tuple[str, str]]):
        return [pair for pair in pairs if all(pair)]
    
    @staticmethod
    def compile_pairs(pairs: List[Tuple[str, str]]):
        """
        pair eg.[("关于下达温州市201([\s\S]{1})年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目")]
        :return:
        """
        return [(re.compile(pair[0]), pair[1]) for pair in pairs]
