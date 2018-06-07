#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_create_script.py

@time: 2018/6/7 上午2:02
"""
from PyScraper.utils import create_gov_script, get_class_source


def test_create_script():
    t1 = [["关于下达温州市201*年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目"]]
    
    result = create_gov_script('test_create_gov_script', t1, 'http://wzkj.wenzhou.gov.cn/', '859905874@qq.com')
    
    content = get_class_source(result)
    assert "关于下达温州市201[\s\S]{1}年公益性科技计划项目" in content
    assert 'http://wzkj.wenzhou.gov.cn/' in content
    assert '859905874@qq.com' in content
    assert result is not None
    try:
        result2 = create_gov_script(None, t1, 'http://wzkj.wenzhou.gov.cn/', '859905874@qq.com')
    except Exception as e:
        assert str(e) == 'parameters should not be None'
    