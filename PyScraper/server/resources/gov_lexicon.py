#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: gov_lexicon.py

@time: 2018/6/9 下午4:25
"""
from flask import request
from flask_restful import Resource, reqparse

from PyScraper.server.resource_handlers.gov_lexicon_handler import GovLexiconHandler

import logging

logger = logging.getLogger(__name__)


class GovLexicon(Resource):
    def get(self):
        result = GovLexiconHandler().get_all_gov_lexicons()
        return result
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gov_rules', type=list, required=True, action='append', help='gov_rules is required')
        args = parser.parse_args()
        gov_rules = args.gov_rules
        result = GovLexiconHandler().create_gov_rules(gov_rules)
        return result
    
    
class GovRule(Resource):
    def delete(self, rule_id):
        result = GovLexiconHandler().delete_gov_rule(rule_id)
        return result
        