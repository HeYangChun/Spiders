# -*- coding: utf-8 -*-
import scrapy
import csv
import sys
import you_get

class HsltSpider(scrapy.Spider):
    name = 'hslt'
    allowed_domains = ['XXXXXXXX']
    start_urls = ['XXXXXXXXXXXXXXXX']
    lstdownloaded = []
    lsttobedownload = []

    def __init__(self):
        ls=self.loadcsv("downloaded.csv")
        self.lstdownloaded=[item[0] for item in ls]
        ls=self.loadcsv("tobedownloaded.csv")
        self.lsttobedownload=[item[0] for item in ls]

    def parse(self, response):
        pass
    
    def loadcsv(self,file):
        ls=[]
        with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            ls.append(row)
        return ls
