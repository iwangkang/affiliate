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
    keyword_index = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword})
    if keyword_index:
        inverted_index = keyword_index.get('invertedIndex')
    return len(inverted_index) or None


def count_merchant_index(merchant):
    """查询所属指定广告主的商品id个数"""
    merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant})
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
    obj_id = MongodbUtil.update('shopping', 'cpc', spec_or_id, document)
    print obj_id


def find_after_sort():
    """查找并排序"""
    products = MongodbUtil.find('shopping', 'product', skip=0, limit=10, sort=[(u'price', -1)])
    print products


def get_price_section(lower_price=None, upper_price=None):
    """获得根据价格区间筛选商品"""
    price_section = None
    if lower_price and upper_price:
        price_section = 'this.price > ' + str(lower_price) + ' & this.productPrice < ' + str(upper_price)
    elif not lower_price and upper_price:
        price_section = 'this.price < ' + str(upper_price)
    elif lower_price and not upper_price:
        price_section = 'this.price > ' + str(lower_price)
    return price_section


def find_where():
    """pymongo中where语句查询"""
    where = get_price_section()
    if where:
        products = MongodbUtil.find('shopping', 'product', {'category': 'Electronics & 3C', '$where': where})
    else:
        products = MongodbUtil.find('shopping', 'product', {'category': 'Electronics & 3C'})
    for product in products:
        print product.get('price')


def find_like():
    """pymongo中like语句查询"""
    result = MongodbUtil.find('shopping', 'keywordIndex', {'keyword': {'$regex': 'cred'}})
    print result


def insert_cps():
    """导入测试cps数据"""
    p_id_list = [
        ObjectId("532281736e292c1130eb3e42"),
        ObjectId("532281736e292c1130eb3e46"),
        ObjectId("532281736e292c1130eb3e56"),
        ObjectId("532281736e292c1130eb3e57"),
        ObjectId("532281736e292c1130eb3e58"),
        ObjectId("532281736e292c1130eb3e59"),
        ObjectId("532281746e292c1130eb3ea8"),
        ObjectId("532281746e292c1130eb3ea6"),
        ObjectId("532281746e292c1130eb3ea3"),
        ObjectId("532281746e292c1130eb3ea2"),
    ]
    for p_id in p_id_list:
        document = {
            'from': 'dx',
            'to': 'FocalPrice',
            'productId': p_id,
            'sellCount': 99,
        }
        print MongodbUtil.insert('shopping', 'cps', document)


def add_total_sell_count():
    """给商品添加总销量统计"""
    # 查询出所有的商品
    product_list = MongodbUtil.find('shopping', 'product')
    # 循环遍历给每个商品添加totalSellCount字段
    for product in product_list:
        cps_total = 0
        # 查询出所有关于该商品的cps统计量，计算总和作为totalSellCount字段的值
        cps_list = MongodbUtil.find('shopping', 'cps', spec_or_id={'productId': product.get('_id')})
        for cps in cps_list:
            cps_total += int(cps.get('sellCount'))
        product['totalSellCount'] = cps_total
        p_id = MongodbUtil.update('shopping', 'product', spec_or_id={'_id': product.get('_id')}, document=product)
        print p_id


def test_group_by():
    """pymongo group by 测试"""
    reduce_cpc_sum_js = """
    function (obj, cpc) {
        if(obj.takeEffect == 1){
            cpc.effectCount++;
        } else if (obj.takeEffect == 0){
            cpc.unEffectCount++;
        }
    }
    """
    results = MongodbUtil.group('shopping', collection='cpc', key=['productId', 'webmaster', 'merchant', 'adPositionId', ],
                                condition={'webmaster': 'xc_shopping'}, initial={'effectCount': 0, 'unEffectCount': 0}, reduce=reduce_cpc_sum_js)
    print results


def test_date_compare():
    """通过时间筛选数据"""
    from datetime import datetime
    # datetime.utcnow()
    begin_date = datetime(2014, 5, 28, 0, 0, 0, 0)
    end_date = datetime(2014, 5, 31, 0, 0, 0, 0)
    result = MongodbUtil.find('api', 'cpc', spec_or_id={'clickTime': {'$gt': begin_date, '$lt': end_date}})
    print result

if __name__ == '__main__':
    test_date_compare()
    # test_group_by()
    # result = MongodbUtil.find('shopping', 'cps', sort=[(u'cpsTime', 1)])
    # print result
    # product_list = MongodbUtil.find('product', spec_or_id={'category': 'Electronics & 3C'}, skip=0, limit=7, sort=[(u'totalSellCount', -1)])
    # print product_list
    # add_total_sell_count()
    # insert_cps()
    # find_after_sort()
    # glossary = MongodbUtil.find_one('glossary')
    # print glossary.get('used')
    # keyword_index = MongodbUtil.find('keywordIndex', spec_or_id={'keyword': {'$regex': 'c'}}, skip=0, limit=1, sort=[(u'searchTimes', -1)])
    # print keyword_index[0].get('keyword')
    # keyword_index = MongodbUtil.find_one('keywordIndex', {'keyword': ''})
    # keyword_index['searchTimes'] += 1
    # MongodbUtil.update('keywordIndex', {'_id': keyword_index.get('_id')}, keyword_index)