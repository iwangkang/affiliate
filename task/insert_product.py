#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-10
@description:插入部分商品
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

from affiliate.task.base import *
from affiliate.task.import_merchant import import_product_id_2_merchant
from affiliate.task.import_product import *
from affiliate.config import settings
from affiliate.lib.util.string_util import StringUtil


@affiliate_celery.task(ignore_result=True)
def insert_product(products, merchant_name):
    """
    指定广告主插入部分商品集合

    """
    try:
        for product in products:
            do_import_product(product, settings.tag_dict)
        import_product_id_2_merchant(merchant_name)
    except Exception as e:
        logger.error('Insert product error: %s' % e.message)


if __name__ == '__main__':
    import time
    print time.time()
    for i in xrange(100000):
        word_str = 'Car  Accessories:Car Alarms & Security'
        word_arr = StringUtil.cut_word(word_str)
    print time.time()
