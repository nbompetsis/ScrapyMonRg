# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    # define the fields for your item here like:
    #constants
    SWITCHES="switches"
    ROUTERS="routers"

    results ={}
    
    #switches = scrapy.Field()
    #routers = scrapy.Field()
    
