# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WzskjjXxgkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    标题 = scrapy.Field()  # 标题
    发布单位 = scrapy.Field()  # 发布时间
    发布日期 = scrapy.Field()  # 发布日期
    url = scrapy.Field()
