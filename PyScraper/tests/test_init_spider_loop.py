#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_start_spider_loop.py

@time: 2018/5/22 上午3:31
"""
from pytest import skip

from PyScraper.spider_loop import start_spider_loop
from PyScraper.utils import run_in_thread
from queue import Queue
import time
def put_spider(queue):
    while True:
        queue.put('22')
        time.sleep(5)
# @skip
def test_start_spider_loop():
    queue = Queue()
    
    run_in_thread(start_spider_loop, queue)
    run_in_thread()