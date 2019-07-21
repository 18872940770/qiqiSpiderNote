# -*- coding: utf-8 -*-
from pprint import pprint

import scrapy, json, time
from copy import deepcopy


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://m.qidian.com/category/male']

    def __init__(self):
        self.base_url = "https://m.qidian.com"
        self.count = 0
        self.other_url = "https://m.qidian.com/majax/category/list?{}&gender=male&pageNum={}&orderBy=&{}&{}"
        self.img_url = "https://bookcover.yuewen.com/qdbimg/349573/{}/150"
        self.other_detail_url = "/book/{}"

    def parse(self, response):
        """解析分类页面"""
        # 获取小说一级分类
        cate_one_list = response.xpath("//div[@class='module module-merge']/ul[@class='sort-ul']/li")
        for cate_one in cate_one_list:
            item = {}
            item["name_one"] = cate_one.xpath(".//h3/text()").extract_first()
            # 获取二级小说分类
            cate_two_list = cate_one.xpath(".//div[@class='sort-li-detail']/a")
            for cate_two in cate_two_list:
                item["list_url"] = self.base_url + cate_two.xpath("./@href").extract_first()
                item["cate_two_name"] = cate_two.xpath("./text()").extract_first()
                # 请求列表页(item在for循环外定义,为防止提取重复数据,使用深拷贝处理)
                yield scrapy.Request(item["list_url"], meta={"item": deepcopy(item)}, callback=self.parse_list_view)

    def parse_list_view(self, response):
        """解析列表页前20条数据"""
        item = response.meta.get("item")
        # 2、获取其他20个加载的列表页数据
        _csrfToken = response.request.headers.get(b'Cookie').decode("utf-8").split(";")[0]
        print(_csrfToken)  # TODO 该token的索引会产生变化，要么0要么1修改即可
        catId = item["list_url"].split("?")[1].split("&")[0]
        subCatId = item["list_url"].split("?")[1].split("&")[1]
        for pagenum in range(2, 10):  # TODO 确定列表页抓取的条数
            other_url = self.other_url.format(_csrfToken, pagenum, catId, subCatId)
            yield scrapy.Request(other_url, meta={"item": deepcopy(item)}, callback=self.other_list_view)

        # 1、默认展示的20条数据
        li_list = response.xpath("//ol[@id='books-']/li")
        for li in li_list:
            item["book_image_url"] = self.base_url + li.xpath(".//a/img/@src").extract_first()
            item["book_detail_url"] = self.base_url + li.xpath(".//a/@href").extract_first()
            item["book_name"] = li.xpath(".//a/img/@alt").extract_first()
            item["book_desc"] = li.xpath(".//p[@class='book-desc']/text()").extract_first().strip()
            item["book_author"] = li.xpath(".//aria[@id='ARIA_author_0']/text()").extract_first()
            print()
            pprint("*默认*" * 100)
            pprint(item)
            self.count += 1
            print("item个数", self.count)

    def other_list_view(self, response):
        """解析列表页后20条数据"""
        item = response.meta.get("item")
        other_data_list = json.loads(response.body.decode()).get('data').get('records')
        for other_data in other_data_list:
            item["book_image_url"] = self.img_url.format(other_data.get('bid'))
            item["book_detail_url"] = self.base_url + self.other_detail_url.format(other_data.get('bid'))
            item["book_name"] = other_data.get('bName')
            item["book_desc"] = other_data.get('desc')
            item["book_author"] = other_data.get('bAuth')
            self.count += 1
            print("=加载=" * 100)
            pprint(item)
            print("item个数", self.count)
