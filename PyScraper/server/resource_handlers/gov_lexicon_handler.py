#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: gov_lexicon_handler.py

@time: 2018/6/9 下午4:00
"""
from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.lexicon import GovLexicon


class GovLexiconHandler:
    def get_all_gov_lexicons(self):
        all = GovLexicon.query.all()
        
        return convert_query_result2dict(all)
    
    def create_gov_rule(self, rule_pair):
        pattern, correct_word = rule_pair
        rule = GovLexicon(pattern=pattern, correct_word=correct_word)
        db.session.add(rule)
        db.session.commit()
        return convert_query_result2dict(rule)
    
    def create_gov_rules(self, rule_pairs):
        return [self.create_gov_rule(rule_pair) for rule_pair in rule_pairs]
        
    def delete_gov_rule(self, rule_id):
        rule = GovLexicon.query.filter_by(rule_id).first()
        db.session.delete(rule)
        db.session.commit()
        return rule_id
    
    def delete_gov_rules(self, rule_ids):
        result = [self.delete_gov_rule(rule_id) for rule_id in rule_ids]
        return result