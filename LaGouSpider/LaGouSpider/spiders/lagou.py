# -*- coding: utf-8 -*-
from pprint import pprint
import scrapy
count = 0
page = 0

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/040000%252C00,000000,0000,00,9,99,Python%2B%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        """提取数据"""
        # 1、提取第一页数据
        div_list = response.xpath("//div[@id='resultList']//div[@class='el']")

        for div in div_list:
            item = {}
            item["station"] = div.xpath("./p[@class='t1 ']/span[1]/a/@title").extract_first()
            item["company"] = div.xpath("./span[@class='t2']/a/text()").extract_first()
            item["detail_url"] = div.xpath(".//a/@href").extract_first()
            item["address"] = div.xpath("./span[@class='t3']/text()").extract_first()
            item["salary"] = div.xpath("./span[@class='t4']/text()").extract_first()
            item["publish_time"] = div.xpath("./span[@class='t5']/text()").extract_first()
            # 2、提取详情页数据
            yield scrapy.Request(item.get("detail_url"), callback=self.detail_parse, meta={"item": item})

        # 3、获取下一页url地址
        next_url = response.xpath("//div[@class='p_in']/ul/li[last()]/a/@href").extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def detail_parse(self, response):
        """提取详情页数据"""
        item = response.meta.get("item")
        item["salary"] = response.xpath("//div[@class='cn']/strong/text()").extract_first()
        item["title"] = response.xpath("//p[@class='msg ltype']/@title").extract_first()
        item["pos_request"] = response.xpath("//div[@class='bmsg job_msg inbox']/p/text()").extract()
        item["work_address"] = response.xpath("//div[@class='bmsg inbox']/p[@class='fp']/text()").extract()

        yield item




