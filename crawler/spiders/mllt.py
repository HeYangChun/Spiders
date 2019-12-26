# -*- coding: utf-8 -*-
import scrapy
import time
import random
from scrapy.loader import ItemLoader
from crawler.items import LtImgItem

class MlltSpider(scrapy.Spider):

    name = 'mllt'

    def start_requests(self):
        #if True:
        #Directly access
        urls=[
            'https://www.mala.cn/forum.php?mod=forumdisplay&fid=17&filter=typeid&typeid=1094'
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parsepagelist)
            # yield scrapy.Request(url=url,callback=self.parsepage)
        #else:
            #Post a request
        #    urls=[
        #        'https://www.mala.cn/forum.php',
        #    ]
        
        #    data={
        #        'mod':'forumdisplay',
        #        'fid':'17',
        #        'filter':'typeid',
        #        'typeid':'1094',
        #    }

        #    for url in urls:
        #        yield  scrapy.FormRequest(url=url,formdata=data,callback=self.parsepagelist)


    def parsepagelist(self, response):
        #BGN:TEST
        #subpagelink = response.xpath("//a[@class='s xst']")[8].xpath("@href").get()
        #yield response.follow(response.urljoin(subpagelink), self.parsepage)
        #return
        #END:TEST
        #find all subpage in the list
        for pgselector in response.xpath("//a[@class='s xst']"):
            subpagelink = pgselector.xpath("@href").get()
            print("subpagelink : %s" % subpagelink)
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
        # print("########")
        # # // *[ @ id = "aimg_12759126"]
        # for sel in response.xpath("//img[@aid]").getall():
        #     print(sel)
        # print("########")
        itemLoader=ItemLoader(item=LtImgItem(),response=response)
        itemLoader.add_xpath('image_urls',"//img[@aid]/@file")
        # itemLoader.add_xpath('image_urls',"//img[@class='zoom']/@file")
        itemLoader.add_value("page_url",response.url)
        yield itemLoader.load_item()

        # check if there is a next page
        nextpages = response.xpath("//a[@class='nxt']")
        for nextpage in nextpages:
           label = nextpage.xpath("text()").get()
           if label.find("下一页") >= 0:
               nextpageurl = nextpage.xpath("@href").get()
               yield response.follow(response.urljoin(nextpageurl), self.parsepage)
