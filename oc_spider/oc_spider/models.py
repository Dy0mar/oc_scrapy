# -*- coding: utf-8 -*-
import random
import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, PrimaryKeyConstraint, Float,
    Text)

Base = declarative_base()


class Category(Base):
    __tablename__ = 'oc_category'

    category_id = Column(Integer, primary_key=True)
    image = Column(String)
    parent_id = Column(Integer)
    top = Column(Integer)
    column = Column(Integer)
    sort_order = Column(Integer)
    status = Column(Integer)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, category_id, image, parent_id, top, column, sort_order,
                 status, date_added, date_modified):
        self.category_id = category_id
        self.image = image
        self.parent_id = parent_id
        self.top = top
        self.column = column
        self.sort_order = sort_order
        self.status = status
        self.date_added = date_added
        self.date_modified = date_modified

    def __repr__(self):
        return "<category_id %s>" % self.category_id

    @classmethod
    def from_item(cls, last_obj, parent):
        data = dict()
        data['category_id'] = last_obj.category_id + 1
        data['image'] = ''
        data['parent_id'] = parent
        data['top'] = 1
        data['column'] = 1
        data['sort_order'] = last_obj.sort_order + 1
        data['status'] = 1
        data['date_added'] = datetime.datetime.utcnow()
        data['date_modified'] = datetime.datetime.utcnow()
        return cls(**data)


class CategoryDescription(Base):
    __tablename__ = 'oc_category_description'
    __table_args__ = (
        PrimaryKeyConstraint('category_id', 'language_id'),
    )

    category_id = Column(
        Integer,
        ForeignKey("oc_category.category_id")
    )
    language_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    meta_title = Column(String)
    meta_description = Column(Integer)
    meta_keyword = Column(String)

    def __init__(self, category_id, language_id, name, description,
                 meta_title, meta_description, meta_keyword):

        self.category_id = category_id
        self.language_id = language_id
        self.name = name
        self.description = description
        self.meta_title = meta_title
        self.meta_description = meta_description
        self.meta_keyword = meta_keyword

    def __repr__(self):
        return "<Data %s, %s>" % (self.category_id, self.name)

    @classmethod
    def from_item(cls, last_obj, language_id, name):
        data = dict()
        data['category_id'] = last_obj.category_id
        data['language_id'] = language_id
        data['name'] = name
        data['description'] = name
        data['meta_title'] = name
        data['meta_description'] = ''
        data['meta_keyword'] = ''
        return cls(**data)


class CategoryToStore(Base):
    __tablename__ = 'oc_category_to_store'
    __table_args__ = (
        PrimaryKeyConstraint('category_id', 'store_id'),
    )

    category_id = Column(
        Integer,
        ForeignKey("oc_category.category_id")
    )
    store_id = Column(Integer)

    def __init__(self, category_id, store_id):

        self.category_id = category_id
        self.store_id = store_id

    def __repr__(self):
        return "<Data %s, %s>" % (self.category_id, self.store_id)

    @classmethod
    def from_item(cls, category_id, store_id):
        data = dict()
        data['category_id'] = category_id
        data['store_id'] = store_id
        return cls(**data)


class Product(Base):
    __tablename__ = 'oc_product'

    product_id = Column(Integer, primary_key=True)
    model = Column(String)
    sku = Column(String)
    upc = Column(String)
    ean = Column(String)
    jan = Column(String)
    isbn = Column(String)
    mpn = Column(String)
    location = Column(String)
    quantity = Column(Integer)
    stock_status_id = Column(Integer)
    image = Column(String)
    manufacturer_id = Column(Integer)
    shipping = Column(Integer)
    price = Column(Float)
    points = Column(Integer)
    tax_class_id = Column(Integer)
    date_available = Column(DateTime, default=datetime.datetime.utcnow)
    weight = Column(Float)
    weight_class_id = Column(Integer)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    length_class_id = Column(Integer)
    subtract = Column(Integer)
    minimum = Column(Integer)
    sort_order = Column(Integer)
    status = Column(Integer)
    viewed = Column(Integer)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow)
    skip_import = Column(Integer, default=0)

    def __init__(self, product_id, model, sku, upc, ean, jan, isbn, mpn,
                 location, quantity, stock_status_id, image, manufacturer_id,
                 shipping, price, points, tax_class_id, date_available, weight,
                 weight_class_id, length, width, height, length_class_id,
                 subtract, minimum, sort_order, status, viewed, date_added,
                 date_modified):

        self.product_id = product_id
        self.model = model
        self.sku = sku
        self.upc = upc
        self.ean = ean
        self.jan = jan
        self.isbn = isbn
        self.mpn = mpn
        self.location = location
        self.quantity = quantity
        self.stock_status_id = stock_status_id
        self.image = image
        self.manufacturer_id = manufacturer_id
        self.shipping = shipping
        self.price = price
        self.points = points
        self.tax_class_id = tax_class_id
        self.date_available = date_available
        self.weight = weight
        self.weight_class_id = weight_class_id
        self.length = length
        self.width = width
        self.height = height
        self.length_class_id = length_class_id
        self.subtract = subtract
        self.minimum = minimum
        self.sort_order = sort_order
        self.status = status
        self.viewed = viewed
        self.date_added = date_added
        self.date_modified = date_modified

    def __repr__(self):
        return "<Data %s>" % self.product_id

    @classmethod
    def from_item(cls, last_obj, item):
        data = dict()
        data['product_id'] = last_obj.product_id + 1
        data['model'] = ''
        data['sku'] = ''
        data['upc'] = ''
        data['ean'] = ''
        data['jan'] = ''
        data['isbn'] = ''
        data['mpn'] = ''
        data['location'] = ''
        data['quantity'] = random.randint(300, 1000)
        data['stock_status_id'] = last_obj.stock_status_id
        data['image'] = item['img_path']
        data['manufacturer_id'] = last_obj.manufacturer_id
        data['shipping'] = last_obj.shipping
        data['price'] = item['price']
        data['points'] = last_obj.points
        data['tax_class_id'] = last_obj.tax_class_id
        data['date_available'] = datetime.datetime.utcnow()
        data['weight'] = last_obj.weight
        data['weight_class_id'] = last_obj.weight_class_id
        data['length'] = last_obj.length
        data['width'] = last_obj.width
        data['height'] = last_obj.height
        data['length_class_id'] = last_obj.length_class_id
        data['subtract'] = last_obj.subtract
        data['minimum'] = last_obj.minimum
        data['sort_order'] = last_obj.sort_order
        data['status'] = 1
        data['viewed'] = last_obj.viewed
        data['date_added'] = last_obj.date_added
        data['date_modified'] = last_obj.date_modified
        return cls(**data)


class ProductDescription(Base):
    __tablename__ = 'oc_product_description'
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'language_id'),
    )

    product_id = Column(
        Integer,
        ForeignKey("oc_product.product_id")
    )
    language_id = Column(Integer)
    name = Column(String)
    fimage = Column(Text, default='')
    video1 = Column(Text, default='')
    html_product_shortdesc = Column(Text, default='')
    html_product_right = Column(Text, default='')
    html_product_tab = Column(Text, default='')
    tab_title = Column(Text, default='')
    description = Column(Text)
    tag = Column(Text, default='')
    meta_title = Column(Text)
    meta_description = Column(Text, default='')
    meta_keyword = Column(Text, default='')

    def __init__(self, product_id, language_id, name, description,
                 html_product_shortdesc, meta_title):

        self.product_id = product_id
        self.language_id = language_id
        self.name = name
        self.description = description
        self.html_product_shortdesc = html_product_shortdesc
        self.meta_title = meta_title

    def __repr__(self):
        return "<Data %s>" % self.product_id

    @classmethod
    def from_item(cls, last_obj, item, language_id):
        data = dict()
        data['product_id'] = last_obj.product_id
        data['language_id'] = language_id
        data['name'] = item['name']
        data['description'] = item['description']
        data['html_product_shortdesc'] = item['product_desc_short']
        data['meta_title'] = item['name']
        return cls(**data)


class ProductToCategory(Base):
    __tablename__ = 'oc_product_to_category'
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'category_id'),
    )

    product_id = Column(
        Integer,
        ForeignKey("oc_product.product_id")
    )
    category_id = Column(Integer)

    def __init__(self, product_id, category_id):

        self.product_id = product_id
        self.category_id = category_id

    def __repr__(self):
        return "<Data %s>" % self.product_id

    @classmethod
    def from_item(cls, last_obj, category_id):
        data = dict()
        data['product_id'] = last_obj.product_id
        data['category_id'] = category_id
        return cls(**data)


class ProductImage(Base):
    __tablename__ = 'oc_product_image'

    product_image_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    image = Column(String)
    sort_order = Column(Integer)

    def __init__(self, product_image_id, product_id, image, sort_order):

        self.product_image_id = product_image_id
        self.product_id = product_id
        self.image = image
        self.sort_order = sort_order

    def __repr__(self):
        return "<Data %s>" % self.product_id

    @classmethod
    def from_item(cls, product_image_id, last_obj, item):
        data = dict()
        data['product_image_id'] = product_image_id
        data['product_id'] = last_obj.product_id
        data['image'] = item['img_path']
        data['sort_order'] = 0
        return cls(**data)


class ProductToStore(Base):
    __tablename__ = 'oc_product_to_store'
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'store_id'),
    )
    product_id = Column(Integer, primary_key=True)
    store_id = Column(Integer)

    def __init__(self, product_id, store_id):

        self.product_id = product_id
        self.store_id = store_id

    def __repr__(self):
        return "<Data %s>" % self.product_id

    @classmethod
    def from_item(cls, product_id, store_id):
        data = dict()
        data['product_id'] = product_id
        data['store_id'] = store_id
        return cls(**data)
