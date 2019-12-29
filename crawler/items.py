# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LtImgItem(scrapy.Item):
    page_url    = scrapy.Field()
    image_urls  = scrapy.Field()

def removeSlashes(url):
    print("removeSlashes url:%s" % url)
    if url.startswith("//"):
        return "https:" + url
    else:
        return url

class TpyLtImgItem(scrapy.Item):
    page_url    = scrapy.Field()
    image_urls  = scrapy.Field(
        input_processor = MapCompose(removeSlashes)
    )