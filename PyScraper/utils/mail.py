#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: mail.py

@time: 2018/5/24 下午9:49
"""

from jinja2 import Template

from PyScraper.settings import MAIL_TEMPLATES_PATH


def render_error_correction_result_mail(title, url, table_head, table_data):
    with open(MAIL_TEMPLATES_PATH, "r") as f:
        raw_html = f.read()
    template = Template(raw_html)
    result = template.render(url=url, title=title, table_head=table_head, table_data=table_data)
    return result