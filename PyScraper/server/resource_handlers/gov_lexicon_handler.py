#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: gov_lexicon_handler.py

@time: 2018/6/9 下午4:00
"""
import logging
from urllib.parse import urlparse

from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.lexicon import GovLexicon

logger = logging.getLogger(__name__)


class GovLexiconHandler:
    def get_all_gov_lexicons(self):
        all = GovLexicon.query.all()
        
        return convert_query_result2dict(all)
    
    def create_gov_rule(self, pattern, correct_word, domain):
        domain = urlparse(domain).netloc
        rule = GovLexicon(pattern=pattern, correct_word=correct_word, domain=domain)
        db.session.add(rule)
        db.session.commit()
        return convert_query_result2dict(rule)
    
    def create_gov_rules(self, rule_pairs):
        logger.info(rule_pairs)
        return [self.create_gov_rule(pattern, correct_word, domain) for (pattern, correct_word, domain) in rule_pairs]
    
    def delete_gov_rule(self, rule_id):
        rule = GovLexicon.query.filter_by(rule_id=rule_id).first()
        db.session.delete(rule)
        db.session.commit()
        return rule_id
    
    def delete_gov_rules(self, rule_ids):
        result = [self.delete_gov_rule(rule_id) for rule_id in rule_ids]
        return result
    
    def get_all_rules_by_domain(self, domain):
        all = GovLexicon.query.filter_by(domain=domain).all()
        return [(one.pattern, one.correct_word) for one in all]
