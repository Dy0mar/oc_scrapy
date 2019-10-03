# -*- coding: utf-8 -*-
import re
import logging
import scrapy

from lxml import html, etree
from oc_spider.items import CategoryItem, ProductItem, ImageItem
from .spider_setting import urls


class BBSpider(scrapy.Spider):
    name = "bb_spider"
    start_urls = urls
    # количество товаров на странице не более чем
    count_product_on_page = 400

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.ERROR)
        super(BBSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        root = html.fromstring(response.body, "lxml")
        for box in root.xpath("//div[@class='shop-by__box']"):

            # check child
            child_cats = box.xpath(".//a[@class='shop-by__link']")
            if not child_cats:
                continue

            el = box.xpath("./a/svg-border")[0]
            parent_category_name = el.get('header').replace('\'', '')

            item = CategoryItem()
            item['name'] = parent_category_name
            item['parent'] = ''
            yield item

        for box in root.xpath("//div[@class='shop-by__box']"):
            # check child
            child_cats = box.xpath(".//a[@class='shop-by__link']")
            if not child_cats:
                continue

            el = box.xpath("./a/svg-border")[0]
            parent_category_name = el.get('header').replace('\'', '')

            for child_cat in child_cats:

                category_name = child_cat.text.replace(',', '')

                item = CategoryItem()
                item['name'] = category_name
                item['parent'] = parent_category_name
                yield item

                category_url = '{}?size={}'.format(
                    child_cat.get('href'), self.count_product_on_page
                )
                yield response.follow(
                    category_url, callback=self.parse_category,
                    cb_kwargs={
                        'parent_category_name': parent_category_name,
                        'category_name': category_name
                    }
                )

    def parse_category(self, response, parent_category_name, category_name):
        root = html.fromstring(response.body, "lxml")
        for a in root.xpath("//a[@class='product__name']"):
            product_url = a.get('href')
            yield response.follow(
                product_url, callback=self.parse_product,
                cb_kwargs={
                    'parent_category_name': parent_category_name,
                    'category_name': category_name
                }
            )

    def parse_product(self, response, parent_category_name, category_name):
        root = html.fromstring(response.body, "lxml")
        product_name = root.xpath(
            "//h1[@class='Product__name']/span[1]")[0].text

        product_name = product_name.strip().encode('ascii', 'ignore')

        # Product__desc-short
        product_desc_short = root.xpath(
            "//div[@class='Product__desc-short']")
        if product_desc_short:
            product_desc_short = product_desc_short[0].text
        else:
            product_desc_short = ''
        #
        product_desc_long = root.xpath(
            "//div[@class='Product__desc-long']")

        if product_desc_long:
            try:
                product_desc_long = product_desc_long[0].text
                product_desc_short = '{} <br> {}'.format(
                    product_desc_short.encode('ascii', 'ignore'),
                    product_desc_long.encode('ascii', 'ignore')
                )
            except UnicodeEncodeError:
                debug = True

        product_description = ''
        for el in root.xpath("//div[@id='vendor-content']"):
            try:
                etree.strip_tags(el, 'a', 'img', 'sup')
            except ValueError:
                debug = True

            tmp = etree.tostring(el, pretty_print=True)
            product_description = '{}{}'.format(
                product_description.encode('ascii', 'ignore'),
                tmp
            )

        product_price = None
        try:
            product_price = root.xpath(
                "//*[@class='sku-chooser__sale-price ']")[0].text
            product_price = product_price.strip().replace('$', '')
        except IndexError:
            # from js
            tmp = root.xpath("//script[contains(text(), 'price')]")[0]
            text = [
                x.replace("'", "") for x in tmp.text.split('\n')
                if 'price' in x
            ][0]
            try:
                product_price = float(''.join(re.findall(r'[\d\.]', text)))
            except TypeError:
                debug = True

        img = root.xpath("//img[@class='Product__img']")[0]

        img_url = img.attrib.get('src')
        if not img_url:
            debug = True
            print ("Skip product - img url not found")

        elif not product_price:
            debug = True
            print ("Skip product - price not found")

        else:
            item = ImageItem()
            item['image_urls'] = [img_url]
            item['parent_category_name'] = parent_category_name
            item['category_name'] = category_name
            yield item

            img_name = img.attrib.get('src').split('/').pop()
            img_path = '{}/{}/{}/{}'.format(
                'catalog', parent_category_name, category_name, img_name
            )

            item = ProductItem()
            item['name'] = product_name
            item['description'] = product_description
            item['product_desc_short'] = product_desc_short
            item['price'] = product_price
            item['img_path'] = img_path
            item['category_name'] = category_name
            yield item
