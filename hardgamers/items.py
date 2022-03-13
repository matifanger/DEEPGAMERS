# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HardgamersItem(scrapy.Item):
    image = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    store = scrapy.Field()
    productID = scrapy.Field()
