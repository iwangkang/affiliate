#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-2
@description:更新产品搜索优先级
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.lib.util.math_util import MathUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def do_update_priority(product):
    """更新产品优先级  优先级=1/关键词数 + 商品价格*点击数 + 1/keywordList.index"""
    try:
        keyword_list = product.get('keywordList')
        product_price = float(product.get('productPrice'))
        #获取该商品总的点击数
        cpc_list = MongodbUtil.find('cpc', {'cpcProductId': product.get('_id')})
        cpc_count = 1
        cpc_active_count = 1
        for cpc in cpc_list:
            cpc_count += int(cpc.get('cpcCount'))
            cpc_active_count += int(cpc.get('cpcActiveCount'))
        cpc_average_count = float(cpc_count + cpc_active_count) / 2.0
        # 更新每个产品的keywordList的每个keyword中产品的优先级
        index = 1
        for keyword in keyword_list:
            priority = 1.0 / float(len(keyword_list)) + MathUtil.parse2percent(product_price * cpc_average_count) + 1.0 / float(index)
            index += 1
            keyword_index = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
            keyword_index['invertedIndex'][product.get('_id').__str__()] = priority
            obj_id = MongodbUtil.save('keywordIndex', keyword_index)
            if obj_id:
                logger.info('Update %s\'s priority successfully!!!' % keyword)
            else:
                logger.info('Update %s\'s priority failed!!!' % keyword)
    except Exception as e:
        logger.error(e.message)


def update_priority():
    """多线程同步更新商品优先级"""
    product_list = MongodbUtil.find('product')
    for product in product_list:
        do_update_priority(product)

