#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: result_handler.py

@time: 2018/6/6 上午2:07
"""

import datetime
import logging
from urllib.parse import urlparse

import cchardet as chardet
import requests
from sqlalchemy import JSON
from sqlalchemy import func
from sqlalchemy.sql.expression import cast

from PyScraper.server.extensions import db
from PyScraper.server.models.base import convert_query_result2dict
from PyScraper.server.models.result import Result

logger = logging.getLogger(__name__)


class ResultHandler:
    def get(self, project_id, limit=10, offset=0):
        all = Result.query.filter_by(project_id=project_id).order_by(
            Result.update_timestamp.desc()).limit(limit).offset(offset).all()
        all_dict = convert_query_result2dict(all)
        result = {
            'total_count': self.count(project_id=project_id),
            'count': len(all),
            'result': all_dict,
        }
        return result
    
    def delete(self, result_id):
        result = Result.query.filter_by(result_id=result_id).first()
        db.session.delete(result)
        db.session.commit()
        return result_id
    
    def deletes(self, project_id, type):
        result = Result.query.filter_by(project_id=project_id).all()
        filter_result = [one for one in result if one.result.get('type') == type]
        logger.info(filter_result)
        for r in filter_result:
            db.session.delete(r)
        db.session.commit()
        return {'project_id': project_id, 'type': type}
    
    def get_gov_error_word(self, project_id):
        all = Result.query.filter_by(project_id=project_id).order_by(
            Result.update_timestamp.desc()).all()
        all_dict = convert_query_result2dict(all)
        type_filter = 'error_word'
        filter_dict = list(filter(lambda one: one.get('result', {}).get('type', '') == type_filter, all_dict))
        result = {
            'total_count': self.count(project_id=project_id),
            'count': len(all),
            'result': filter_dict,
        }
        return result
    
    def get_gov_error_link(self, project_id):
        all = Result.query.filter_by(project_id=project_id).order_by(
            Result.update_timestamp.desc()).all()
        all_dict = convert_query_result2dict(all)
        type_filter = 'error_link'
        filter_dict = list(filter(lambda one: one.get('result', {}).get('type', '') == type_filter, all_dict))
        result = {
            'total_count': self.count(project_id=project_id),
            'count': len(all),
            'result': filter_dict,
        }
        return result
    
    def put_result(self, project_id, result, increment=False):
        if increment:
            result_item = Result.query.filter_by(project_id=project_id, result=cast(result, JSON)).first()
            if result_item:
                result_item.update_timestamp = datetime.datetime.now()
            else:
                result_item = Result(project_id=project_id, result=result)
        else:
            result_item = Result(project_id=project_id, result=result)
        db.session.add(result_item)
        db.session.commit()
        return project_id
    
    def count(self, project_id):
        if project_id:
            return db.session.query(func.count(Result.result_id)).filter_by(project_id=project_id).scalar()
        else:
            return db.session.query(func.count(Result.result_id)).scalar()
    
    def grounding_sourcecode_cache(self, result_id):
        """
        渲染当时爬取的网页源码并给出标红的源码
        :return:
        """
        result_item = Result.query.filter_by(result_id=result_id).first()
        result = result_item.result
        
        url = result['url']
        previous_url = result['previous_url']
        
        content = result['previous_content']
        
        return self.grounding_sourcecode(content, url, previous_url)
    
    def grounding_sourcecode_realtime(self, result_id):
        """
        实时地渲染网页并给出标红的源码
        目前只支持直接进行http1.1请求得到源码，
        不支持浏览器渲染后得到源码的方式
        :param result_id:
        :return:
        """
        result_item = Result.query.filter_by(result_id=result_id).first()
        result = result_item.result
        
        previous_url = result['previous_url']
        url = result['url']
        
        r = requests.get(previous_url)
        
        codings = chardet.detect(r.content)
        if codings and codings.get('encoding'):
            r.encoding = codings['encoding']
        content = r.text
        
        return self.grounding_sourcecode(content, url, previous_url)

    def grounding_sourcecode_realtime_error_word(self, result_id, error_word):
        """
        渲染页面，
        标红错误词
        :param result_id:
        :return:
        """
        result_item = Result.query.filter_by(result_id=result_id).first()
        result = result_item.result
    
        url = result['url']
    
        r = requests.get(url)
    
        codings = chardet.detect(r.content)
        if codings and codings.get('encoding'):
            r.encoding = codings['encoding']
        content = r.text

        head = content
        body = ''
        foot = ''
        if error_word in content:
            head, foot = content.split(error_word, maxsplit=1)
            body = "<strong style='color: red'>" + error_word + "</strong>"
            
        return {'previous_url': url, 'content': content, 'head': head, 'body': body, 'foot': foot}
    
    def grounding_sourcecode(self, content, url, previous_url):
        head = content
        body = ''
        foot = ''
        if url in content:
            head, foot = content.split(url, 1)
            body = "<strong style='color: red'>" + url + "</strong>"
        else:
            url = '/' + url.split('/', 3)[3]
            if url in content:
                print(url)
                print(content)
                head, foot = content.split(url, 1)
                body = "<strong style='color: red'>" + url + "</strong>"
        
        # content = re.sub(escaped_url, "<strong id='highlight'>\g<0></strong>", content)
        return {'previous_url': previous_url, 'content': content, 'head': head, 'body': body, 'foot': foot}
