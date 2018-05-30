#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: twisted_utils.py

@time: 2018/5/30 下午7:27
"""
from twisted.internet import reactor
from twisted.internet.defer import Deferred


def aiosleep(secs):
    """
    example usage:
    @inlinecallbacks
    def x():
        yield aiosleep(100)
    """
    d = Deferred()
    reactor.callLater(secs, d.callback, None)
    return d
