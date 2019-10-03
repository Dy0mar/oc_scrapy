# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.pipelines.images import ImagesPipeline

from oc_spider.items import CategoryItem, ProductItem, ImageItem
from oc_spider.models import (
    Category, CategoryDescription, CategoryToStore, Product,
    ProductDescription, ProductToCategory, ProductImage, ProductToStore)
from oc_spider.dump import DATABASES

# TODO:
# поставить дефолт значения в моделях
# set log level


class CrawlImagesPipeline(ImagesPipeline):
    allow_save_image = True

    def get_media_requests(self, item, info):
        if isinstance(item, ImageItem) and self.allow_save_image:
            for image_url in item['image_urls']:
                sub_category = item.get('category_name')

                request = Request(url=image_url, cb_kwargs={
                    'parent_category_name': item['parent_category_name'],
                    'category_name': sub_category
                })
                yield request

    def file_path(self, request, response=None, info=None):
        image_name = request.url.split('/').pop()
        sub_category = request.cb_kwargs.get('category_name')
        if sub_category:
            path = '{}/{}/{}'.format(
                request.cb_kwargs.get('parent_category_name'),
                sub_category,
                image_name
            )
        else:
            path = '{}/{}'.format(
                request.cb_kwargs.get('parent_category_name'),
                image_name
            )
        return path


class OcPipeline(object):
    def __init__(self):
        self.engine = create_engine(
            "mysql://{}:{}@{}/{}".format(
                DATABASES['USER'], DATABASES['PASSWORD'],
                DATABASES['HOST'], DATABASES['NAME'],
                ),
            echo=True,
            encoding='utf-8',
        )

        # Initial values
        session = Session(bind=self.engine)
        self.save_counter = 0

        cats = session.query(CategoryDescription).all()
        self.categories = dict()
        for cat in cats:
            self.categories.update({
                cat.name: cat.category_id
            })

        self.last_category = session.query(Category).order_by(
            Category.category_id.desc()
        ).first()
        if not self.last_category:
            self.last_category = 1

        products = session.query(ProductDescription).all()
        self.products = set([x.name for x in products])

        self.last_product = session.query(
            Product).filter_by(status=True).order_by(
            Product.product_id.desc()
        ).first()

        self.language_id = session.query(
            CategoryDescription).order_by(
            CategoryDescription.category_id.desc()
        ).first().language_id

        if not self.language_id:
            self.language_id = 1

        self.store_id = session.query(CategoryToStore).order_by(
            CategoryToStore.category_id.desc()).first().store_id
        if not self.store_id:
            self.store_id = 0

        self.product_image_id = session.query(ProductImage).order_by(
            ProductImage.product_image_id.desc()).first().product_image_id

        if not self.product_image_id:
            self.product_image_id = 1

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            self.process_save_category(item)

        if isinstance(item, ProductItem):
            self.process_save_product(item)

        return item

    # save category item
    def process_save_category(self, item):
        if item['name'] not in self.categories.keys():
            # print(item['parent'], item['name'])
            # Достать category_id
            parent = self.get_category_id(item['parent'])

            # oc_category, update last_category
            self.last_category = Category.from_item(
                self.last_category, parent
            )
            self.session.add(self.last_category)

            # Добавить категорию в словарь, чтобы не доставать id из бд
            self.categories.update({
                item['name']: self.last_category.category_id
            })

            # oc_category_description
            obj = CategoryDescription.from_item(
                self.last_category, self.language_id, item['name']
            )
            self.session.add(obj)

            # oc_category_to_store
            obj = CategoryToStore.from_item(
                self.last_category.category_id, self.store_id
            )
            self.session.add(obj)

    # save product item
    def process_save_product(self, item):

        if item['name'] not in self.products:
            category_id = self.get_category_id(item['category_name'])

            # oc_product
            self.last_product = Product.from_item(self.last_product, item)
            self.session.add(self.last_product)

            # oc_product_description
            obj = ProductDescription.from_item(
                self.last_product, item, self.language_id
            )
            self.session.add(obj)

            # oc_product_to_category
            obj = ProductToCategory.from_item(self.last_product, category_id)
            self.session.add(obj)

            # oc_product_image
            self.product_image_id += 1
            obj = ProductImage.from_item(
                self.product_image_id, self.last_product, item
            )
            self.session.add(obj)

            # oc_product_to_store
            obj = ProductToStore.from_item(
                self.last_product.product_id, self.store_id
            )
            self.session.add(obj)

            self.products.add(item['name'])
            self.save_counter += 1
            if self.save_counter >= 40:
                self.save_counter = 0
                try:
                    s = self.session.commit()
                except InvalidRequestError as e:
                    stop = True
                    print (e.message)
                    raise CloseSpider('Some error')
                print ("{} products write success!".format(self.save_counter))

    def get_category_id(self, category_name):
        if not category_name:
            return 0

        category_id = self.categories.get(category_name)
        if category_id:
            return category_id

        print category_name
        raise CloseSpider('category not defined - {}'.format(category_name))

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)


class DuplicatesPipeline(object):
    def __init__(self):
        self.categories = set()

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            if item['name'] in self.categories:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.categories.add(item['name'])
                return item
        else:
            return item
