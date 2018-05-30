#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_start_spider_loop.py

@time: 2018/5/22 上午3:31
"""

from queue import Queue

from PyScraper.spider_loop import start_spider_loop
from PyScraper.utils import run_in_thread, import_class


def act_example_spider(queue, action):
    item = {'action': action, 'spidercls': 'effective_spiders.test_spiders.example.BlockExampleSpider', 'project_id': '1'}
    queue.put(item)
    print('put spider')




def test_start_spider_loop():
    queue = Queue()
    print('start')
    run_in_thread(start_spider_loop, queue, daemon=False)
    print('put a start spider')
    act_example_spider(queue, action='start')
    print('stop it ')
    act_example_spider(queue, action='stop')
    print('end')


if __name__ == '__main__':
    test_start_spider_loop()
