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
    

class RgItem(scrapy.Item):
    node = scrapy.Field()
    name = scrapy.Field()
    discards = scrapy.Field()
    errors = scrapy.Field()
    broadcastpackets = scrapy.Field()
    multicastpackets = scrapy.Field()
    packetloss = scrapy.Field()
    mem = scrapy.Field()
    packets = scrapy.Field()
    rtt = scrapy.Field()
    traffic = scrapy.Field()
    aggregate = scrapy.Field()
    cpu = scrapy.Field()


