# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class AmazonspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = Field()
    product_review_url = Field()
    product_review = Field()
    review_star = Field()
    review_time = Field()
    useful_num = Field()
