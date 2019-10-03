# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CategoryItem(Item):
    name = Field()
    parent = Field()


class ProductItem(Item):
    name = Field()
    description = Field()
    product_desc_short = Field()
    price = Field()
    img_path = Field()
    category_name = Field()


class ImageItem(Item):
    parent_category_name = Field()
    category_name = Field()
    image_urls = Field()
    images = Field()
