# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv


class PeopleCnPipeline(object):
    def open_spider(self,spider):
        self.out = open("People-美国.csv", "w")
        self.writer = csv.writer(self.out)
        self.writer.writerow(['Headline','Url','Date','Source','Article'])
    def process_item(self, item, spider):

        self.writer.writerow([item['Headline'],item['Url'],item['Date'],
                                 item['Source'], item['Article']])
        return item
    def close_spider(self,spider):
        self.out.close()
