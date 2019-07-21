# -*- coding: utf-8 -*-
from copy import copy

import scrapy
from pprint import pprint

class AreasspiderSpider(scrapy.Spider):
    name = 'areasspider'
    allowed_domains = ['http://www.stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/']

    def __init__(self):
        self.base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'

    def parse_pro(self, response):
        """提取省份信息"""
        # 提取全国省份
        alist = response.xpath("//tr[@class='provincetr']//td//a")
        count = 0
        proList = []
        for a in alist:
            count += 1
            item = {}
            item["ID"] = count
            item["proName"] = a.xpath("./text()").extract_first()
            item["proUrl"] = a.xpath("./@href").extract_first()
            item["parentId"] = None
            pprint(item)
            proList.append(item)
        # 提取市区信息
        for item in proList:

            yield scrapy.Request(item.get("proUrl")+self.base_url, callback=self.parse_city, meta={"item": copy(item), "count":count})


    def parse_city(self, response):
        """提取市区信息"""
        print("进入市区提取函数")
        item = response.meta.get("item")
        count = response.meta.get("count")
        trList = response.xpath("//tr[@class='citytr']//td[2]//a")
        for tr in trList:
            count += 1
            temp = {}
            temp["ID"] = count
            temp["cityName"] = tr.xpath("./text()").extract_first()
            temp["cityUrl"] = tr.xpath("./@href").extract_first()
            temp["parentId"] = item.get("ID")
            pprint(temp)



