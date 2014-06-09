#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-13
@description:cpc异步任务
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


@affiliate_celery.task(ignore_result=True)
def cpc_effect(source, merchant_id, product_id):
    """点击生效更新数据"""
    #TODO


@affiliate_celery.task(ignore_result=True)
def cpc_un_effect(source, merchant_id, product_id):
    """301跳转异常、更新有效点击数"""
    #TODO