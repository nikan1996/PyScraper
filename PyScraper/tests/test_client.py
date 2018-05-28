#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_client.py

@time: 2018/5/28 下午3:02
"""
import pytest

from PyScraper.server.app import create_app


@pytest.fixture
def app():
    return create_app()
    
    
    # def test_app(client):
    # assert client.get(url_for('myview')).status_code == 200
