# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class HsltImagePipeline(ImagesPipeline):
    # def get_media_requests(self, item, info):
    #     print("in get_media_requests")
    #     for image_url in item['image_urls']:
    #         headers = {'referer': item['referer']}
    #         yield Request(image_url, meta={'item': item}, headers=headers)

    # def file_path(self, request, response=None, info=None):
    #     print("in file-path...")
    #     return "/home/andy/temp/"
    pass

