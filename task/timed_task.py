#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-10
@description:定时任务
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.task.clear_product import clear_product
from affiliate.task.update_priority import update_priority
from affiliate.lib.util.date_util import DateUtil


@affiliate_celery.task(ignore_result=True)
def clear_update_product():
    logger.info('[TIME: %s] METHOD: clear_update_product' % DateUtil.get_sys_time())
    update_priority()
    clear_product()