# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class TestbizhiPipeline(ImagesPipeline):
    #def process_item(self, item, spider):
    #    return item
    def get_media_requests(self, item, info):
        for img_url in item['img_url']:
            yield Request(img_url, meta={'name': item['name'], 'img_name': item['img_name']})

    def file_path(self, request, response=None, info=None):
        img_guid = request.url.split('/')[-1]
        name = request.meta['name']
        img_name = request.meta['img_name']
        img_guid = img_guid.replace(img_guid.split('.')[-2], img_name)
        file_name = '{0}/{1}'.format(name, img_guid)
        return file_name

