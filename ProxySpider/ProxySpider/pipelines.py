# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class ProxyspiderPipeline(object):

    def open_spider(self, spider):
        """爬虫初始化"""
        print("*" * 100)
        # 链接mongodb数据库
        self.client = MongoClient(host="127.0.0.1", port=27017)
        self.collection = self.client["scrapy"]["proxy_ip"]

    def process_item(self, item, spider):
        # 将代理ip写入文件
        with open("proxy.txt", "w", encoding="utf-8") as f:
            f.write(item)
        # 将数据存入mongodb
        self.collection.insert(item)
        print("item插入成功！")
        return item

    def close_spider(self, spider):
        print("*" * 100)
