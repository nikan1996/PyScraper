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

class Result(Resource):
    def get(self, project_id):
        args = parser.parse_args()
        limit = args.limit
        offset = (args.page - 1) * limit

        result = ResultHandler().get(project_id=project_id, limit=limit, offset=offset)
        logger.info('get result result:{}'.format(result))
        return result
