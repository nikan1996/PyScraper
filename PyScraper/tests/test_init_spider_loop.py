#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_start_spider_loop.py

@time: 2018/5/22 上午3:31
"""

from queue import Queue

from PyScraper.spider_loop import start_spider_loop
from PyScraper.utils import run_in_thread
from effective_spiders.test_spiders.wzskjj_xxgk.wzskjj_xxgk import Wzskjj_xxgkSpider


def put_spider(queue):
    while True:
        queue.put(Wzskjj_xxgkSpider)
        print('put spider')
        break
        # time.sleep(5)


def test_start_spider_loop():
    queue = Queue()
    print('start')
    run_in_thread(put_spider(queue))
    print('put spider_cls_queue start')
    start_spider_loop(queue)
    print('end')


if __name__ == '__main__':
    test_start_spider_loop()
