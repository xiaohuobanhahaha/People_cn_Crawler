# -*- coding: utf-8 -*-

import scrapy
import json
import jsonpath
import time
import random
from people_cn.items import PeopleCnItem


def Xpath_Build(i):
    i=i+1
    headline = '/html/body/div[3]/div[2]/ul['+str(i)+']/li[1]/b/a'
    url = '/html/body/div[3]/div[2]/ul['+str(i)+']/li[1]/b/a/@href'
    date = '/html/body/div[3]/div[2]/ul['+str(i)+']/li[3]/text()'
    return headline,url,date


def Link_Bulid(num):
    num =num+1
    #美国
    Link = 'http://search.people.com.cn/cnpeople/search.do?pageNum='+str(num)+ \
           '&keyword=%C3%C0%B9%FA&site' \
           'Name=news&facetFlag=true&nodeType=belongsId&nodeId=0'
    # 美方
    #Link = 'http://search.people.com.cn/cnpeople/search.do?pageNum=' +str(num)+\
    #       '&keyword=%C3%C0%B7%BD&site' \
    #       'Name=news&facetFlag=true&nodeType=belongsId&nodeId=0'
    return Link,num

class PeopleSpider(scrapy.Spider):
    name = 'people'
    num=0
    def start_requests(self):
        Link,num = Link_Bulid(self.num)
        yield scrapy.Request(url= Link,callback=self.parse,
                             dont_filter=True,
                             meta={'num': num})

    def parse(self, response):
        if response.status == 200:
            item = PeopleCnItem()
            num=response.meta['num']
            for i in range(20):
                headline,url,date=Xpath_Build(i)
                temp=response.xpath(headline)
                item['Url'] = response.xpath(url).extract()[0]
                item['Headline']=temp.xpath('string(.)').extract()[0]
                item['Date']=response.xpath(date).extract()[0].strip()
                yield item
                #进入链接取出文章内容
                yield scrapy.Request(url=item['Url'],callback=self.page_parse,
                                     meta={'Headline':item['Headline'],
                                           'Date':item['Date'],
                                           'Url':item['Url']})

            if num<3400:
                num += 1
                Link,num = Link_Bulid(num)
                yield scrapy.Request(url=Link, callback=self.parse,
                                     dont_filter=True,
                                     meta={'num': num})

    def page_parse(self, response):
        if response.status == 200:
            item = PeopleCnItem()
            temp=response.xpath('//*[@id="rwb_zw"]')
            try:
                item['Article']=temp.xpath('normalize-space(string(.))').extract()[0].strip()
            except:
                item['Article']=None
            item['Source'] = response.xpath('/html/body/div[4]/div/div[1]/a/text()').extract()[0]
            item['Headline']=response.meta['Headline']
            item['Date']=response.meta['Date']
            item['Url']=response.meta['Url']
            yield item
