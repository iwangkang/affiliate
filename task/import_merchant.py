#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-30
@description:导入广告主
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.config import settings
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def import_merchant():
    """导入广告主"""
    try:
        for merchant in settings.merchant_list:
            merchant_name = merchant.get('name')
            if merchant_name:
                merchant_id, update_flag = MongodbUtil.update_or_insert('merchant', {'name': merchant_name}, {'name': merchant_name})
                if merchant_id:
                    if update_flag:
                        logger.info('Update merchant: %s successfully!!!' % merchant_name)
                    else:
                        logger.info('Save merchant: %s successfully!!!' % merchant_name)
                else:
                    logger.info('Save merchant: %s failed!!!' % merchant_name)
    except Exception as e:
        logger.error(e.message)


def import_product_id_2_merchant(merchant_name):
    """导入广告主下所有产品的id集合"""
    try:
        merchant = MongodbUtil.find_one('merchant', {'name': merchant_name})
        product_list = MongodbUtil.find('product', {'productMerchantId': merchant.get('_id')})
        product_id_list = list()
        for product in product_list:
            product_id_list.append(product.get('_id'))
        merchant['productIdList'] = product_id_list
        merchant_id = MongodbUtil.save('merchant', merchant)
        if merchant_id:
            logger.info('Import product id list to %s successfully!!!' % merchant_name)
        else:
            logger.info('Import product id list to %s failed!!!' % merchant_name)
    except Exception as e:
        logger.error(e.message)
