# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class HsltImagePipeline(ImagesPipeline):
    # def get_media_requests(self, item, info):
    #     print("in get_media_requests")
    #     for image_url in item['image_urls']:
    #         headers = {'referer': item['referer']}
    #         yield Request(image_url, meta={'item': item}, headers=headers)
    def process_item(self,item,spider):
        if item.get('image_urls'):
            urls = item['image_urls']
            item['image_urls']=[url for url in urls if not url.endswith(".gif")]
            #print("Item :{}".format(item['image_urls']))
            return ImagesPipeline.process_item(self,item,spider)
        else:
            raise DropItem("Invalid Item")

    def file_path(self, request, response=None, info=None):
        return request.url.replace("/","_")

    # pass

