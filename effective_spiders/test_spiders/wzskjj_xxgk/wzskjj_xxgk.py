# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse


class WzskjjXxgkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    标题 = scrapy.Field()  # 标题
    发布单位 = scrapy.Field()  # 发布时间
    发布日期 = scrapy.Field()  # 发布日期
    url = scrapy.Field()


class Wzskjj_xxgkSpider(scrapy.Spider):
    zh_cn_name = "温州市科技局_信息公开"
    name = 'wzskjj_xxgk'
    _source_url = ['http://xxgk.wenzhou.gov.cn/col/col1327029/index.html']
    
    def start_requests(self):
        first_page = "http://xxgk.wenzhou.gov.cn/module/xxgk/search.jsp?infotypeId=&vc_title=&vc_number=&vc_filenumber=&area=001008003015006"
        
        yield Request(first_page, callback=self.datail_page, method="post",
                      headers={"Content-Type": "application/x-www-form-urlencoded"},
                      body="infotypeId=0&jdid=2237&divid=div1326694&vc_title=&vc_number=&currpage=&vc_filenumber=&vc_all=&texttype=&fbtime=&infotypeId=&vc_title=&vc_number=&vc_filenumber=&area=001008003015006")
    
    def datail_page(self, response):
        total_page = int(re.findall("(?<!共)(共.+?页)", response.text)[0].split("共")[-1][:-1])
        next_page_base = "http://xxgk.wenzhou.gov.cn/module/xxgk/search.jsp?texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={}&sortfield="
        for num in range(1, total_page + 1):
            next_page = next_page_base.format(num)
            yield Request(next_page, method="post", headers={"Content-Type": "application/x-www-form-urlencoded"},
                          body="infotypeId=&jdid=2497&area=001008003015006&divid=div1326694&vc_title=&vc_number=&currpage=2&vc_filenumber=&vc_all=&texttype=&fbtime=&texttype=&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={}&sortfield=".format(
                              num))
    
    def parse(self, response: TextResponse):
        
        trs = response.selector.css("table > tr > td > table:nth-child(2) > tr")[1:]
        for tr in trs:
            item = WzskjjXxgkItem()
            item['url'] = tr.css("td> a::attr(href)").extract_first()
            item['标题'] = tr.css("td> a::text").extract_first()
            item['发布单位'] = tr.css("td:nth-child(2)::text").extract_first()
            item['发布日期'] = tr.css("td:nth-child(3)::text").extract_first()
            yield item


if __name__ == '__main__':
    settings = {
        "TELNETCONSOLE_ENABLED": False,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(Wzskjj_xxgkSpider)
    process.start()
