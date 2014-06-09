#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-13
@description:mongod测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bson.objectid import ObjectId
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def count_inverted_index(keyword):
    """查询指定关键词商品索引id的个数"""
    keyword_index = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
    if keyword_index:
        inverted_index = keyword_index.get('invertedIndex')
    return len(inverted_index) or None


def count_merchant_index(merchant):
    """查询所属指定广告主的商品id个数"""
    merchant = MongodbUtil.find_one('merchant', {'name': merchant})
    product_id_list = merchant.get('productIdList')
    return len(product_id_list)


def increment_integer():
    """整数自增"""
    spec_or_id = {
        'from': '123456',
        'to': ObjectId('52c4e2276e292c2de4c4a641'),
        'cpcProductId': ObjectId("52c6557b6e292c3484794585")
    }
    document = {'$inc': {'cpcCount': 1, 'cpcActiveCount': -1}}
    obj_id = MongodbUtil.update('cpc', spec_or_id, document)
    print obj_id


if __name__ == '__main__':
    keyword = 'wifi router'
    count = count_inverted_index(keyword)
    print count
    # count = count_merchant_index('FocalPrice')
    # print count