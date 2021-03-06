# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    detail_url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

# class AmazonitemspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     title = scrapy.Field()
#     price = scrapy.Field()
#     file_urls = scrapy.Field()
#     files = scrapy.Field()
