#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: settings.py

@time: 2018/5/23 下午2:52
"""
# Obey robots.txt rules
from os.path import abspath, join, dirname
import os
SETTING_FILE_DIR = dirname(__file__)

ROBOTSTXT_OBEY = False
DOWNLOAD_HANDLERS = {
    'http': 'scrapy.core.downloader.handlers.http.ChromiumDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.ChromiumDownloadHandler',
}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
DEPTH_LIMIT = 0  # no limitation to depth , set positive integer for depth level.
PROXY_ENABLED = False

CONCURRENT_REQUESTS = 100
CONCURRENT_ITEMS = 100

COOKIES_ENABLED = False


FEED_EXPORT_ENCODING = 'utf-8'

CHROMIUM_URL = '127.0.0.1:9000'
TELNETCONSOLE_ENABLED = False
SPIDER_SCRIPT_MODULE = 'effective_spiders'
GOV_SPIDER_DIR = join(os.path.abspath(os.path.join(SETTING_FILE_DIR, os.pardir)), 'effective_spiders', 'gov_spiders')
GOV_SPIDER_MODULE = 'effective_spiders.gov_spiders'
TEMPLATES_DIR = join(dirname(__file__), 'utils', 'templates')
SCRIPT_TEMPLATES_DIR = TEMPLATES_DIR + '/script_templates'
MAIL_TEMPLATES_PATH = TEMPLATES_DIR + '/mail_templates.html'



mail_settings = {
    'smtphost': 'smtp.qq.com',
    'mailfrom': '859905874@qq.com',
    'smtpport': 465,
    'smtpssl': True,
    'smtpuser': '859905874@qq.com',
    'smtppass': 'cgcxzdatxduybbhh',
}
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'test_scrapy_start.middlewares.TestScrapyStartSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'test_scrapy_start.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'test_scrapy_start.pipelines.TestScrapyStartPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
