# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayoffsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    season = scrapy.Field()
    date = scrapy.Field()
    away = scrapy.Field()
    home = scrapy.Field()
    away_score = scrapy.Field()
    home_score = scrapy.Field()
    result = scrapy.Field()
