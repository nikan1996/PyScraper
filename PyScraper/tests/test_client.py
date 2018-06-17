#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_client.py

@time: 2018/5/28 下午3:02
"""
import json

import pytest
import sqlalchemy
from sqlalchemy_utils import database_exists, drop_database

from PyScraper.server.app import create_app


@pytest.fixture
def app():
    print('setup app')
    app = create_app(config='PyScraper.config.TestConfig')
    yield app
    print('tear down app')
    # delete test database
    with app.app_context():
        engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        if database_exists(engine.url):
            drop_database(engine.url)


def dictify(response):
    """Decode json from response"""
    if response.data is None:
        return None
    return json.loads(response.data.decode('utf8'))


def less_equal(dict1: dict, dict2: dict):
    if dict1 is None or dict2 is None:
        return False
    """equal the same key to respect the key less dict"""
    if len(dict1) > len(dict2):
        dict1, dict2 = dict2, dict1
    for key in dict1.keys():
        if dict1[key] != dict2[key]:
            return False
    return True


def test_database_api(client):
    # get the list of databases
    response = client.get('/databases')
    
    assert response.status_code == 200
    assert dictify(response) == []
    
    database_id = 1
    database_name = 'test'
    database_config = {
        'host': 'localhost',
        'port': '3306',
        'user': 'root',
        'password': '123456',
        'database': 'not_avialable_test_pyscraper',
    }
    data = {
        'database_name': 'test',
        'config': database_config
    }
    # get the database
    response = client.get('/database/{}'.format(database_id))
    assert response.status_code == 200
    assert dictify(response) is None
    
    # create database
    post_data = json.dumps(data)
    print(post_data)
    response = client.put('/databases', data=post_data, content_type='application/json')
    print(response.data)
    assert response.status_code == 403
    text = dictify(response)
    print(text)
    
    response = client.get('/database/{}'.format(database_id))
    assert response.status_code == 200
    
    # get all databases
    response = client.get('/databases')
    assert response.status_code == 200
    assert isinstance(dictify(response), list) is True
    
    new_data = {
        'database_name': 'test2',
        'config': database_config
    }
    post_data = json.dumps(new_data)
    response = client.put('/database/{}'.format(database_id), data=post_data, content_type='application/json')
    assert response.status_code == 200
    
    response = client.delete('/database/{}'.format(database_id))
    assert response.status_code == 200
    deleted_data = new_data.copy()
    deleted_data.update({'is_deleted': True})
    
    response = client.get('/database/{}'.format(database_id))
    assert response.status_code == 200
    assert dictify(response) is None


def test_project_api(client):
    # get the list of projects
    response = client.get('/projects')
    
    assert response.status_code == 200
    assert dictify(response) == []
    project_id = 1
    project_name = 'project_1'
    setting = {
        'mail': {
            'account': 'test@qq.com',
            'password': 'asdf$#@asd'  # usually authorization code in almost email servers
        },
        "spidercls": "effective_spiders.test_spiders.example.ExampleSpider"
    }
    cron_config = {
        'cron_time': 10,
        'crontab_expressions': '* * * * *'
    }
    tag = 'tag_1'
    data = {
        'project_name': project_name,
        'setting': setting,
        'cron_config': cron_config,
        'tag': tag,
    }
    post_data = json.dumps(data)
    response = client.put('/projects', data=post_data, content_type='application/json')
    assert response.status_code == 200
    text = dictify(response)
    assert less_equal(text, data)
    
    response = client.get('/project/{}'.format(project_id))
    assert response.status_code == 200
    assert less_equal(dictify(response), data)
    
    # get all databases
    response = client.get('/projects')
    assert response.status_code == 200
    assert isinstance(dictify(response), list) is True
    assert less_equal(dictify(response)[0], data) is True
    
    new_data = data.copy()
    new_data['project_name'] = 'project_2'
    post_data = json.dumps(new_data)
    response = client.put('/project/{}'.format(project_id), data=post_data, content_type='application/json')
    assert less_equal(dictify(response), new_data)
    
    response = client.delete('/project/{}'.format(project_id))
    deleted_data = new_data.copy()
    deleted_data.update({'is_deleted': True})
    assert less_equal(dictify(response), deleted_data)
    
    response = client.get('/project/{}'.format(project_id))
    assert response.status_code == 200
    assert dictify(response) is None


def test_task_api(client):
    # get the list of tasks
    response = client.get('/task/1?limit=10&page=1')
    assert response.status_code == 200
    
    
def test_result_api(client):
    # get the list of tasks
    response = client.get('/result/1?limit=10&page=1')
    assert response.status_code == 200


def test_statistics_api(client):
    response = client.get('/statistics')
    assert response.status_code == 200
    _dict = {
        "project_num": 0,
        "running_project_num": 0,
        "all_result_num": 0
    }
    assert less_equal(dictify(response), _dict)