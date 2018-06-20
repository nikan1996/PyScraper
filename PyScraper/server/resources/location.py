#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: location.py

@time: 2018/6/18 下午9:51
"""
import logging

from flask_restful import Resource, reqparse

from PyScraper.server.resource_handlers.result_handler import ResultHandler

logger = logging.getLogger(__name__)


class Location(Resource):
    def get(self, result_id):
        type_parser = reqparse.RequestParser()
        type_parser.add_argument('type', type=str, required=True)
        type_parser.add_argument('error_word', type=str)
        type_parser_args = type_parser.parse_args()
        if type_parser_args.error_word:
            return ResultHandler().grounding_sourcecode_realtime_error_word(result_id, error_word=type_parser_args.error_word)
        if type_parser_args.type == 'cache':
            return ResultHandler().grounding_sourcecode_cache(result_id)
        elif type_parser_args.type == 'real':
            return ResultHandler().grounding_sourcecode_realtime(result_id)
        elif type_parser_args.type:
            return "请附带正确的type类型"
