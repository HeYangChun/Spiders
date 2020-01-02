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
    crawlAll = False
    cntoflstpgcrawled = 0

    custom_settings = {
        "IMAGES_STORE": "/home/andy/workspace/picsfrmnetmllt_temp"
    }

    def start_requests(self):
        self.urlAccessed = utilities.readFile(self.fileLogURLAccessed)
        self.crawlAll = ( len(self.urlAccessed) <= 0 )

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

                # check if all pages are needed to be crawled
                self.cntoflstpgcrawled = self.cntoflstpgcrawled + 1
                if not self.crawlAll:
                    if self.cntoflstpgcrawled >= 10:
                        print("pages enough for updating!")
                        break

               yield response.follow(response.urljoin(nextpageurl), self.parsepagelist)
               break

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
