#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_blank_html.py

@time: 2018/6/8 下午6:12
"""
from PyScraper.extractor.blank_html import BlankHtmlExtractor


def test_blank_html_1():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

</body>
</html>"""
    ble = BlankHtmlExtractor()
    ble.is_blank()
    
    
def test_blank_html_2():
    html = """"""
    