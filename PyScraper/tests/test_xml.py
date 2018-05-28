#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: test_xml.py

@time: 2018/5/26 下午7:03
"""

# abs_path =
import json
import time
from urllib.parse import urljoin

import requests
import xmltodict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from os.path import dirname, abspath, join
import re

from PyScraper.extractor.xml_link import DataProxyXmlLinkExtractor


r = requests.get("http://wzkj.wenzhou.gov.cn/module/jpage/dataproxy.jsp?page=2&appid=1&appid=1&webid=1934&path=/&columnid=1389975&unitid=4455560&webname=%E6%B8%A9%E5%B7%9E%E5%B8%82%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%B1%80&permissiontype=0")
print(r.text)
et = DataProxyXmlLinkExtractor()
print(et.dataproxy_xml_extract(r.text))