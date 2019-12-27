# -*- coding: utf-8 -*-
import scrapy
import time
import random
import os
from scrapy.loader import ItemLoader
from crawler.items import LtImgItem
import crawler.utilities as utilities

class MlltSpider(scrapy.Spider):

    name = 'mllt'
    flnmLogURLAccessed="urlaccessedurl_mllt.txt"
    fileLogURLAccessed = os.getcwd() + "/" + flnmLogURLAccessed
    urlAccessed=[]

    def start_requests(self):
        self.urlAccessed = utilities.readFile(self.fileLogURLAccessed)

        urls=[
            'https://www.mala.cn/forum.php?mod=forumdisplay&fid=17&filter=typeid&typeid=1094'
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parsepagelist)

    def parsepagelist(self, response):
        #find all subpage in the list
        for pgselector in response.xpath("//a[@class='s xst']"):
            subpagelink = pgselector.xpath("@href").get()
            # Filter page link that had been accessed
            if self.__isthisaccessed(subpagelink):
                print("Page had been accessed:%s" % subpagelink)
                continue

            # parse pagea
            self.__markthisasaccessed(subpagelink)

            yield response.follow(response.urljoin(subpagelink), self.parsepage)

        #find next page:
        nextpages = response.xpath("//a[@class='nxt']")
        for nextpage in nextpages:
           label=nextpage.xpath("text()").get()
           if label.find("下一页") >= 0:
               nextpageurl = nextpage.xpath("@href").get()
               yield response.follow(response.urljoin(nextpageurl), self.parsepagelist)


    def parsepage(self,response):
        #find all images
        itemLoader=ItemLoader(item=LtImgItem(),response=response)
        itemLoader.add_xpath('image_urls',"//img[@aid]/@file")
        itemLoader.add_value("page_url",response.url)
        yield itemLoader.load_item()

        # check if there is a next page
        nextpages = response.xpath("//a[@class='nxt']")
        for nextpage in nextpages:
           label = nextpage.xpath("text()").get()
           if label.find("下一页") >= 0:
               nextpageurl = nextpage.xpath("@href").get()
               yield response.follow(response.urljoin(nextpageurl), self.parsepage)

    def __isthisaccessed(self,url):
        return url in self.urlAccessed

    def __markthisasaccessed(self,url):
        self.urlAccessed.append(url)
        utilities.fileAppend(self.fileLogURLAccessed, url)
