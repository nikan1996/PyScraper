#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_email.py

@time: 2018/5/24 下午8:43
"""
import pytest
import pytest_twisted
from scrapy.mail import MailSender
from twisted.internet import reactor
from twisted.internet.defer import Deferred

from PyScraper.utils.mail import render_mail


def aiosleep(secs):
    d = Deferred()
    reactor.callLater(secs, d.callback, None)
    return d


@pytest.fixture
def mailer():
    return MailSender(smtphost='smtp.qq.com', mailfrom='859905874@qq.com', smtpport=465,
                      smtpssl=True, smtpuser='859905874@qq.com', smtppass='cgcxzdatxduybbhh')


@pytest.fixture
def rendered_html_table_email():
    render_dict = {
        'title': '（PyScraper发送）错误网站',
        'table_head': ['正确词', '错误词', '网站地址'],
        'table_data': [
            {'correct': '中华人民共和国', 'error': '中黑人民共和国', 'url': 'http://www.w3school.com.cn/tags/tag_table.asp'},
            {'correct': '中华人民共和国', 'error': '中白人民共和国', 'url': 'http://www.w3school.com.cn/tags/tag_table.asp'},
            {'correct': '中华人民共和国', 'error': '中黄人民共和国', 'url': 'http://www.w3school.com.cn/tags/tag_table.asp'},
        ]}
    return render_mail(render_dict['title'], render_dict['table_head'], render_dict['table_data'])


@pytest.mark.skip
@pytest_twisted.inlineCallbacks
def test_send_qq_email(mailer):
    yield mailer.send(to=["859905874@qq.com"], subject='Test', body='HELLO', )


@pytest.mark.skip
@pytest_twisted.inlineCallbacks
def test_send_html_table_email(mailer, rendered_html_table_email):
    yield mailer.send(to=["859905874@qq.com"], subject='（PyScraper发送）错误网站', body=rendered_html_table_email, mimetype='text/html')
