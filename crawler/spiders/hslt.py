# -*- coding: utf-8 -*-
import scrapy
import time
import random
from scrapy.loader import ItemLoader
from crawler.items import hsltImgItem

class HsltSpider(scrapy.Spider):
    name = 'hslt'

    def start_requests(self):
        urls=[
            'http://bbs.voc.com.cn/forum-50-1.html',
            'http://bbs.voc.com.cn/forum-22-1.html',
            # 'http://bbs.voc.com.cn/topic-9086035-1-1.html'
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parsepagelist)

    def __takearest(self):
        time.sleep(random.random()*3)

    def parsepagelist(self, response):
        #find all subpage in the list
        for pgselector in response.xpath("//a[@href][@class][@title]"):
            subpagelink = pgselector.xpath("@href").get()
            #parse page
            self.__takearest()
            yield response.follow(response.urljoin(subpagelink), self.parsepage)

        #find next page:
        nextpages = response.xpath("//a[@class='p_redirect']")
        for nextpage in nextpages:
            label=nextpage.xpath("text()").get()
            if label.find("下一页") >= 0:
                nextpageurl = nextpage.xpath("@href").get()
                self.__takearest()
                yield response.follow(response.urljoin(nextpageurl), self.parsepagelist)


    def parsepage(self,response):
        #Find all image in this page
        # imgsrcs=response.xpath("//img[@onload]/@src").getall()
        # for imgsrc in imgsrcs:
        #     yield {"imgsrc":response.urljoin(imgsrc)}

        itemLoader=ItemLoader(item=hsltImgItem(),response=response)
        itemLoader.add_xpath('image_urls',"//img[@onload]/@src")
        yield itemLoader.load_item()

        #check if there is a next page
        nextpages = response.xpath("//a[@class='p_redirect']")
        for nextpage in nextpages:
            label = nextpage.xpath("text()").get()
            if label.find("下一页") >= 0:
                nextpageurl = nextpage.xpath("@href").get()
                yield response.follow(response.urljoin(nextpageurl), self.parsepage)
