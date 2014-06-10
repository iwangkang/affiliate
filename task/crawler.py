#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-2-13
@description:保存爬取productFeed信息
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config import settings
from affiliate.config.celeryconfig import affiliate_celery
from affiliate.lib.util.logger_util import logger
from affiliate.task.import_product import do_import_product


@affiliate_celery.task(ignore_result=True)
def crawling(product):
    """
    将页面js爬取的productFeed保存入库

    """
    try:
        if isinstance(product, dict):
            do_import_product(product, settings.tag_dict)
    except Exception as e:
        logger.error('Crawling error: %s' % e.message)