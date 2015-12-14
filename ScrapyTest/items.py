# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

"""The docstring of the item.py.

It has the scrapy results of parsing native objects.

"""

import scrapy


# define the fields for your item here like

class ScrapytestItem(scrapy.Item):
    """ScrapytestItem class defines the fields of first items."""

    SWITCHES = "switches"
    ROUTERS = "routers"


# Class for the results of the parsing

class NativeObjectItem(scrapy.Item):
    """NativeObjectItem class defines the fields of native objects."""

    native_id = scrapy.Field()
    uri = scrapy.Field()
    metadata = scrapy.Field()
