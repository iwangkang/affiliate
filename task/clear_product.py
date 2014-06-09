#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-31
@description:清理过期产品
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def clear_product():
    """清理过期产品"""
    try:
        product_list = MongodbUtil.find('product')
        today = DateUtil.get_sys_date()
        for product in product_list.__iter__():
            start_date = product.get('productStartTime')
            alive_time = product.get('productAliveTime')
            end_date = DateUtil.get_end_date(start_date, alive_time)
            if today > end_date:
                product_id = product.get('_id')
                #删除product
                MongodbUtil.delete('product', product)
                logger.info('Delete a product: %s successfully!!!' % product.get('productTitle'))
                #删除索引中product.id
                keyword_list = product.get('keywordList')
                for keyword in keyword_list:
                    keyword = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
                    if not keyword:
                        continue
                    if keyword['invertedIndex'].__contains__(product_id.__str__()):
                        del keyword['invertedIndex'][product_id.__str__()]
                        MongodbUtil.save('keywordIndex', keyword)
                        logger.info('Update keyword index: %s successfully!!!' % keyword)
                #删除merchant中product.id
                # TODO
                #删除product的image及图片文件
                MongodbUtil.delete('image', {'imageProductId': product_id})
    except Exception as e:
        logger.error(e.message)