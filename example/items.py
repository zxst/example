# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CFDAItem(scrapy.Item):
    # define the fields for your item here like:
    news_url = scrapy.Field()

    news_title = scrapy.Field()

    news_date = scrapy.Field()

    site_url = scrapy.Field()

    content_len = scrapy.Field()

    html_file_url = scrapy.Field()
