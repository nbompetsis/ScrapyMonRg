# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    # define the fields for your item here like:
    # Constants of the class
    SWITCHES="switches"
    ROUTERS="routers"
    

class NativeObjectItem(scrapy.Item):
    native_id = scrapy.Field()
    uri = scrapy.Field()
    metadata = scrapy.Field()


