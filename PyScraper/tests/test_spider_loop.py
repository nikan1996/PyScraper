#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_start_spider_loop.py

@time: 2018/5/22 上午3:31
"""

from queue import Queue

import time

from PyScraper.spider_loop import start_spider_loop
from PyScraper.utils import run_in_thread, import_class


def act_example_spider(queue, action, spidercls, project_id):
    item = {'action': action, 'spidercls': spidercls, 'project_id': project_id}
    queue.put(item)
    print('put spider')


def test_start_spider_loop():
    queue = Queue()
    thread = run_in_thread(start_spider_loop, queue, daemon=True)
    act_example_spider(queue, action='start', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider',
                       project_id=1)
    act_example_spider(queue, action='stop', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider',
                       project_id=1)
    
    act_example_spider(queue, action='start', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider2',
                       project_id=2)
    
    act_example_spider(queue, action='pause', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider2',
                       project_id=2)
    act_example_spider(queue, action='start', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider2',
                       project_id=2)
    act_example_spider(queue, action='stop', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider2',
                       project_id=2)
    
    act_example_spider(queue, action='start', spidercls='effective_spiders.test_spiders.example.BlockExampleSpider2',
                       project_id=2)

    time.sleep(10)


if __name__ == '__main__':
    test_start_spider_loop()
