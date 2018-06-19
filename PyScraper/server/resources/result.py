#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: result.py

@time: 2018/6/6 上午2:13
"""

import logging

from flask_restful import Resource, reqparse

from PyScraper.server.resource_handlers.result_handler import ResultHandler

logger = logging.getLogger(__name__)

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, required=True, help='limit is required')
parser.add_argument('page', type=int, required=True, help='page is required')

type_parser = reqparse.RequestParser()
type_parser.add_argument('type', type=str)


class Results(Resource):
    def get(self, project_id):
        type_parser_args = type_parser.parse_args()
        
        if type_parser_args.type == 'error_word':
            return ResultHandler().get_gov_error_word(project_id)
        elif type_parser_args.type == 'error_link':
            return ResultHandler().get_gov_error_link(project_id)
        elif type_parser_args.type:
            return "请附带正确的type类型"
        
        args = parser.parse_args()
        limit = args.limit
        offset = (args.page - 1) * limit
        
        result = ResultHandler().get(project_id=project_id, limit=limit, offset=offset)
        logger.info('get result result:{}'.format(result))
        return result
    
    def delete(self, project_id):
        type_parser_args = type_parser.parse_args()
        
        if type_parser_args.type == 'error_word' or 'error_link':
            result = ResultHandler().deletes(project_id=project_id, type=type_parser_args.type)
            logger.info('delete results result:{}'.format(result))
            return result
        elif type_parser_args.type:
            return "请附带正确的type类型"
        



class Result(Resource):
    def delete(self, result_id):
        result = ResultHandler().delete(result_id)
        return result
