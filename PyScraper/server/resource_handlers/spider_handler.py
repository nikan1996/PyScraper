#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: spider_handler.py

@time: 2018/6/2 上午4:26
"""

from PyScraper.settings import SPIDER_SCRIPT_MODULE
from PyScraper.utils import load_spiders, walk_modules, get_full_classname


class SpiderHandler:
    def get_all_spiders(self):
        modules = walk_modules(SPIDER_SCRIPT_MODULE)
        spiders = load_spiders(submodules=modules)
        return [(spider.name, get_full_classname(spider)) for spider in spiders]
    
    def create_spider(self):
        pass
    
    def delete_spider(self):
        """
        spider may not be deleted actually instead backup it
        :return:
        """
        pass
