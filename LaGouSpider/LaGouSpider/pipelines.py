# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pprint

import re
from pymongo import MongoClient


class LagouspiderPipeline(object):
    def __init__(self):
        self.count = 0

    def open_spider(self, spider):
        """爬虫初始化"""
        print("*" * 100)
        # 链接mongodb数据库
        self.client = MongoClient(host="127.0.0.1", port=27017)
        self.collection = self.client["scrapy"]["jobs_51"]

    def process_item(self, item, spider):
        """数据清洗与保存"""
        item["title"] = re.sub(r"\xa0", "", item.get("title"))
        item["work_address"] = "".join([i.strip() for i in item.get("work_address") if len(i.strip()) > 0])
        regex = [re.sub(r"\xa0", "", i) for i in item.get("pos_request") if len(re.sub(r"\xa0", "", i)) > 0]
        item["pos_request"] = regex if regex else None
        self.count += 1
        print("item个数", self.count)

        # 将数据存入mongodb
        # self.collection.insert(item)
        pprint(item)


    def close_spider(self, spider):
        """爬取结束设置"""
        print("-" * 100)
