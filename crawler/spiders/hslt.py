# -*- coding: utf-8 -*-
import scrapy
import time
import random
import os
from scrapy.loader import ItemLoader
from crawler.items import LtImgItem
import crawler.utilities as utilities


class HsltSpider(scrapy.Spider):
    name = 'hslt'
    flnmLogURLAccessed="urlaccessedurl_hslt.txt"
    fileLogURLAccessed = os.getcwd() + "/" + flnmLogURLAccessed
    urlAccessed=[]

    def start_requests(self):
        self.urlAccessed = utilities.readFile(self.fileLogURLAccessed)

        urls=[
            'http://bbs.voc.com.cn/forum-50-1.html',
            #'http://bbs.voc.com.cn/forum-22-1.html',
            #'http://bbs.voc.com.cn.forum-72-1.html',
            # 'http://bbs.voc.com.cn/topic-9086035-1-1.html'
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parsepagelist)

    # def __takearest(self):
    #     time.sleep(random.random()*3)

    def parsepagelist(self, response):
        #find all subpage in the list
        for pgselector in response.xpath("//a[@href][@class][@title]"):
            subpagelink = pgselector.xpath("@href").get()
            #Filter page link that had been accessed
            if self.__isthisaccessed(subpagelink):
                print("Page had been accessed:%s" % subpagelink)
                continue

            #parse pagea
            self.__markthisasaccessed(subpagelink)

            #get it
            yield response.follow(response.urljoin(subpagelink), self.parsepage)

        #find next page:
        nextpages = response.xpath("//a[@class='p_redirect']")
        for nextpage in nextpages:
            label=nextpage.xpath("text()").get()
            if label.find("下一页") >= 0:
                nextpageurl = nextpage.xpath("@href").get()
                # self.__takearest()
                yield response.follow(response.urljoin(nextpageurl), self.parsepagelist)


    def parsepage(self,response):
        #Find all image in this page
        # imgsrcs=response.xpath("//img[@onload]/@src").getall()
        # for imgsrc in imgsrcs:
        #     yield {"imgsrc":response.urljoin(imgsrc)}

        itemLoader=ItemLoader(item=LtImgItem(),response=response)
        itemLoader.add_xpath('image_urls',"//img[@onload]/@src")
        itemLoader.add_value("page_url",response.url)
        yield itemLoader.load_item()

        #check if there is a next page
        nextpages = response.xpath("//a[@class='p_redirect']")
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
