#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: gov_lexicon.py

@time: 2018/6/9 下午4:25
"""

from flask_restful import Resource

from PyScraper.server.resource_handlers.gov_lexicon_handler import GovLexiconHandler


class GovLexicon(Resource):
    def get(self):
        result = GovLexiconHandler().get_all_gov_lexicons()
        return result
    
    def put(self, pairs):
        result = GovLexiconHandler().create_gov_rules(pairs)
        return result
