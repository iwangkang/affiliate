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
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def import_merchant(merchant_name):
    """导入广告主"""
    try:
        import_flag = False
        if merchant_name:
            merchant_id, update_flag = MongodbUtil.update_or_insert('shopping', 'merchant', {'name': merchant_name}, {'name': merchant_name})
            if merchant_id:
                import_flag = True
                if update_flag:
                    logger.info('Update merchant: %s successfully!!!' % merchant_name)
                else:
                    logger.info('Save merchant: %s successfully!!!' % merchant_name)
            else:
                logger.info('Save merchant: %s failed!!!' % merchant_name)
        return import_flag
    except Exception as e:
        logger.error(e.message)


def import_product_id_2_merchant(merchant_name):
    """导入广告主下所有产品的id集合"""
    try:
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant_name})
        product_list = MongodbUtil.find('shopping', 'product', {'merchantId': merchant.get('_id')})
        product_id_list = list()
        for product in product_list:
            product_id_list.append(product.get('_id'))
        merchant['productIdList'] = product_id_list
        merchant_id = MongodbUtil.save('shopping', 'merchant', merchant)
        if merchant_id:
            logger.info('Import product id list to %s successfully!!!' % merchant_name)
        else:
            logger.info('Import product id list to %s failed!!!' % merchant_name)
    except Exception as e:
        logger.error(e.message)
