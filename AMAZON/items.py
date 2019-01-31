# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    label = scrapy.Field()
    ASIN = scrapy.Field()
    product_star = scrapy.Field()
    product_fit = scrapy.Field()
    product_fit_info = scrapy.Field()
    product_ask_num = scrapy.Field()
    product_review_num = scrapy.Field()
    is_best_seller = scrapy.Field()
    best_seller_title = scrapy.Field()
    total_rank = scrapy.Field()
    total_rank_info = scrapy.Field()
    detail_rank = scrapy.Field()
    detail_rank_info = scrapy.Field()

