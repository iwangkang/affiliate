#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-5
@description:初始化Mongodb
"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo

from affiliate.config import settings
from affiliate.lib.model.mongod.base import Base


def init_index(db):
    if db == settings.shopping_dbname:  # index of shopping
        shopping_db = Base.client[db]
        shopping_db.fs.files.ensure_index('filename', name='filename', unique=True, background=True)

        shopping_db.image.ensure_index('productId', name='productId', background=True)
        shopping_db.image.ensure_index('fileName', name='fileName', unique=True, background=True)

        shopping_db.keywordIndex.ensure_index('keyword', name='keyword', unique=True, background=True)

        shopping_db.merchant.ensure_index('name', name='name', unique=True, backgroud=True)

        shopping_db.product.ensure_index('merchantId', name='merchantId', background=True)
        shopping_db.product.ensure_index('startTime', name='startTime', background=True)
        shopping_db.product.ensure_index('price', name='price', background=True)
        shopping_db.product.ensure_index('category', name='category', background=True)
        shopping_db.product.ensure_index([('productId', pymongo.ASCENDING), ('merchantId', pymongo.ASCENDING)],
                                         unique=True, backgroud=True)
        shopping_db.cpc.ensure_index('productId', name='productId', background=True)
        shopping_db.cpc.ensure_index('webmaster', name='webmaster', background=True)
        shopping_db.cpc.ensure_index('merchant', name='merchant', background=True)
        shopping_db.cpc.ensure_index('adPositionId', name='adPositionId', background=True)
        shopping_db.cpc.ensure_index('clickTime', name='clickTime', background=True)
        shopping_db.cpc.ensure_index(
            [('productId', pymongo.ASCENDING), ('webmaster', pymongo.ASCENDING), ('merchant', pymongo.ASCENDING)],
            backgroud=True)

        shopping_db.cps.ensure_index('sku', name='sku', background=True)
        shopping_db.cps.ensure_index('cpcId', name='cpcId', background=True)
        shopping_db.cps.ensure_index('webmaster', name='webmaster', background=True)
        shopping_db.cps.ensure_index('merchant', name='merchant', background=True)
    elif db == settings.api_dbname:  # index of api
        api_db = Base.client[db]
        api_db.cpc.ensure_index('uid', name='uid', background=True)
        api_db.cpc.ensure_index('webmaster', name='webmaster', background=True)
        api_db.cpc.ensure_index('merchant', name='merchant', background=True)
        api_db.cpc.ensure_index('url', name='url', background=True)
        api_db.cpc.ensure_index('clickTime', name='clickTime', background=True)
        api_db.cpc.ensure_index('language', name='language', background=True)
        api_db.cpc.ensure_index('category', name='category', background=True)
        api_db.cpc.ensure_index([('uid', pymongo.ASCENDING), ('clickTime', pymongo.ASCENDING), ('webmaster', pymongo.ASCENDING), ('merchant', pymongo.ASCENDING)], unique=True, backgroud=True)

        api_db.cps.ensure_index('orderId', name='orderId', background=True)
        api_db.cps.ensure_index('cpcId', name='cpcId', background=True)
        api_db.cps.ensure_index('orderTime', name='orderTime', background=True)
        api_db.cps.ensure_index('merchant', name='merchant', background=True)
        api_db.cps.ensure_index([('orderId', pymongo.ASCENDING), ('merchant', pymongo.ASCENDING)], unique=True, backgroud=True)


if __name__ == "__main__":
    init_index('shopping')