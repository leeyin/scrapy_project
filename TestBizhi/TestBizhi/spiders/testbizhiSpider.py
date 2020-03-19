# !/usr/bin/python3
"""
CreateTime：2020/3/19 11:44
@Author：Leeya
"""
import scrapy
from TestBizhi.items import TestbizhiItem


class TestBizhiSpider(scrapy.Spider):
    name = 'testbizhiSpider'
    allowed_domains = ['desk.zol.com.cn']
    #start_urls = ['http://desk.zol.com.cn/bizhi/8755_107821_2.html',
    #              'http://desk.zol.com.cn/bizhi/8752_107788_2.html']

    start_urls = ['http://desk.zol.com.cn/pc/']

    def parse(self, response):
        base_url = 'http://desk.zol.com.cn'
        list = response.css('.photo-list-padding a::attr(href)').getall()
        for img in list:
            url = base_url + img    # 每组图片第一张的地址
            next_url =response.css('#pageNext::attr(href)').get()
            if next_url is not None:
                next_url = base_url + next_url
                yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(url, callback=self.content)

    def content(self, response):
        img_list = response.css('#showImg a::attr(href)').getall()
        for image in img_list:
            img_url = response.url.replace(response.url.split('/')[-1], image.split('/')[-1])
            self.log('新的img_url:%s' % img_url)
            yield scrapy.Request(img_url, callback=self.content)

        item = TestbizhiItem()
        item['img_url'] = response.css('#bigImg::attr(src)').getall()
        item['name'] = response.css('#titleName::text').get()
        item['img_name'] = response.css('.current-num::text').get()
        yield item



class TestBizhiSpider_2(scrapy.Spider):
    name = 'testbizhiSpider_2'
    allowed_domains = ['desk.zol.com.cn']
    start_urls = ['http://desk.zol.com.cn/bizhi/8755_107821_2.html',
                  'http://desk.zol.com.cn/bizhi/8752_107788_2.html']

    def parse(self, response):
        list = response.css('#showImg a::attr(href)').getall()
        for img in list:
            img_url = response.url.replace(response.url.split('/')[-1], img.split('/')[-1])
            self.log('新的img_url:%s' % img_url)
            yield scrapy.Request(img_url, callback=self.parse)
        item = TestbizhiItem()
        item['img_url'] = response.css('#bigImg::attr(src)').getall()
        item['name'] = response.css('#titleName::text').get()
        item['img_name'] = response.css('.current-num::text').get()
        yield item


class TestBizhiSpider_1(scrapy.Spider):
    name = 'testbizhiSpider_1'
    allowed_domains = ['desk.zol.com.cn']
    start_urls = ['http://desk.zol.com.cn/bizhi/8755_107821_2.html',
                  'http://desk.zol.com.cn/bizhi/8752_107788_2.html']

    def parse(self, response):
        item = TestbizhiItem()
        item['img_url'] = response.css('#bigImg::attr(src)').getall()
        item['name'] = response.css('#titleName::text').get()
        item['img_name'] = response.css('.current-num::text').get()
        yield item
