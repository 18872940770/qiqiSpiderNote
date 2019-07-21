# -*- coding: utf-8 -*-
import scrapy


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/']

    def __init__(self):
        """初始化"""
        self.base_url = "https://www.xicidaili.com"

    def parse(self, response):
        """爬取xici网上国内高匿代理"""
        # 爬取第一页数据
        tr_list = response.xpath("//table[@id='ip_list']/tr")[1:]
        for tr in tr_list:
            item = {}
            item["ip"] = tr.xpath(".//td[2]/text()").extract_first()
            item["port"] = tr.xpath(".//td[3]/text()").extract_first()
            item["type"] = tr.xpath(".//td[6]/text()").extract_first()
            print(item)

        # 爬取下页数据
        next_url = self.base_url + response.xpath("//div[@class='pagination']/a[@class='next_page']/@href").extract_first()
        yield scrapy.Request(next_url, callback=self.parse)

