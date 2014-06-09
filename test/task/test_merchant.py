#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-30
@description:广告主测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.import_merchant import import_merchant, import_product_id_2_merchant


def test_import_merchant():
    import_merchant()


def test_import_product_id_2_merchant(merchant_name):
    import_product_id_2_merchant(merchant_name)


if __name__ == '__main__':
    # test_import_merchant()
    test_import_product_id_2_merchant('FocalPrice')
