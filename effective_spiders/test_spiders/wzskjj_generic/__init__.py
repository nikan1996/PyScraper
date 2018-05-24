#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: __init__.py.py

@time: 2018/5/24 下午12:37
"""
with open("关于下达温州市2016年公益性科技计划项目及经费的通知.html", 'r') as f:
    content = f.read()

import re

rules = [
    ("关于下达温州市201([\s\S]{1})年公益性科技计划项目", "关于下达温州市2017年公益性科技计划项目")
]
import time

pattern1 = re.compile("关于下达温州市201[\s\S]{1}年公益性科技计划项目")

start = time.process_time()

correct_set = {"关于下达温州市2017年公益性科技计划项目"}
result = pattern1.findall(content)
result = set(result)
print(time.process_time()-start)
print(result - correct_set)
print(result)
