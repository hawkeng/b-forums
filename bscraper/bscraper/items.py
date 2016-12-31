# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ForumTable(scrapy.Item):
    name = scrapy.Field()
    content = scrapy.Field()
    detail = scrapy.Field()