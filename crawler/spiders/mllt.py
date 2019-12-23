# -*- coding: utf-8 -*-
import scrapy


class MlltSpider(scrapy.Spider):
    name = 'mllt'
    allowed_domains = ['https://photo.mala.cn/']
    start_urls = ['http://https://photo.mala.cn//']

    def parse(self, response):
        pass
