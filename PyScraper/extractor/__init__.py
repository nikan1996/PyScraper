#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: __init__.py.py

@time: 13/03/2018 2:14 PM
"""

from urllib.parse import urljoin
# 将可能是相对的url转化为 绝对url
print(urljoin('http://zskjj.zhoushan.gov.cn/col/col1312724/index.html?uid=4271661&pageNum=4', "/art/2018/5/21/art_1312724_18191956.html"))