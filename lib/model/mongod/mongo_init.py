#coding=utf8
__author__ = 'changdongsheng'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo

from affiliate.lib.model.mongod.base import Base


def init_index():
    Base.db.fs.files.ensure_index('filename', name='filename', unique=True, background=True)
    Base.db.keywordIndex.ensure_index('keyword', name='keyword', unique=True, background=True)
    Base.db.product.ensure_index('productMerchantId', name='productMerchantId', background=True)
    Base.db.product.ensure_index([('productId', pymongo.ASCENDING), ('productMerchantId', pymongo.ASCENDING)],
                                 unique=True, backgroud=True)
    Base.db.cpc.ensure_index([('from', pymongo.ASCENDING), ('to', pymongo.ASCENDING),
                              ('cpcProductId', pymongo.ASCENDING)], unique=True, background=True)


init_index()


if __name__ == "__main__":
    init_index()