# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeopleCnItem(scrapy.Item):
    Url = scrapy.Field()
    Headline = scrapy.Field()
    Date=scrapy.Field()
    Article = scrapy.Field()
    Source = scrapy.Field()
