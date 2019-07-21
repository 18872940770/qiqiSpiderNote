# -*- coding: utf-8 -*-
import json
from pprint import pprint

import re
import scrapy


class CompanyinfoSpider(scrapy.Spider):
    name = 'companyinfo'
    allowed_domains = ['gov.cn']
    start_urls = ['http://deal.ggzy.gov.cn/ds/deal/dealList.jsp']

    def __init__(self):
        self.des_url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
        self.params = "TIMEBEGIN_SHOW=2019-03-22&TIMEEND_SHOW=2019-03-31&TIMEBEGIN=2019-03-22&TIMEEND=2019-03-31&SOURCE_TYPE=1&DEAL_TIME=02&DEAL_CLASSIFY=00&DEAL_STAGE=0000&DEAL_PROVINCE=0&DEAL_CITY=0&DEAL_PLATFORM=0&BID_PLATFORM=0&DEAL_TRADE=0&isShowAll=1&PAGENUMBER={}&FINDTXT=&validationCode="
        self.count = 0
        self.headers = {"Referer": "http://www.ggzy.gov.cn/information/html/a/430000/0201/201903/29/0043a6d26645ebb9454885bc42e5ebcc8871.shtml"}

    def parse(self, response):
        """向目标网站发起post请求"""
        for num in range(1, 183):
            params = self.params.format(num)
            formdata = {param.split("=")[0]: param.split("=")[1] for param in params.split("&")}
            yield scrapy.FormRequest(
                self.des_url,
                formdata=formdata,
                callback=self.parse_des_url
            )

    def parse_des_url(self, response):
        """解析目标网址"""
        # 获取列表页数据
        item_list = json.loads(response.body.decode()).get("data")
        for item in item_list:
            # 拼接详情页请求网址
            detail_url = re.sub(r"/a/", "/b/", item.get("url"))
            # 获取详情页数据
            yield scrapy.Request(detail_url, meta={"item": item}, callback=self.parse_detail_url, headers=self.headers)

    def parse_detail_url(self, response):
        """获取详情页"""
        item = response.meta.get("item")
        item["detail"] = [i.strip() for i in response.xpath("//span/text()").extract()]
        yield item

