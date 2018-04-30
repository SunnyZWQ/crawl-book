# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Comment(scrapy.Item):
    book = scrapy.Field()
    user = scrapy.Field()
    rate = scrapy.Field()
    date = scrapy.Field()


class Book(scrapy.Item):
    tag = scrapy.Field()
    name = scrapy.Field()
    rate = scrapy.Field()
    comment_num = scrapy.Field()
    rate5 = scrapy.Field()
    rate4 = scrapy.Field()
    rate3 = scrapy.Field()
    rate2 = scrapy.Field()
    rate1 = scrapy.Field()
    author = scrapy.Field()
    original_name = scrapy.Field()
    translator = scrapy.Field()
    public_year = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    bookType = scrapy.Field()
    packing = scrapy.Field()
    ISBN = scrapy.Field()
    comment_link = scrapy.Field()
