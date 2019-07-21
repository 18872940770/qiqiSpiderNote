# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pprint import pprint


class CompanyinfospiderPipeline(object):
    def open_spider(self, spider):
        self.count = 0

    def process_item(self, item, spider):
        self.count += 1
        pprint(item)
        print("item个数", self.count)
        return item

    def close_spider(self, spider):
        print("*"*100)