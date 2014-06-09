#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-9
@description:定时清理产品测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.clear_product import clear_product


def test_clear_product():
    clear_product()


if __name__ == '__main__':
    test_clear_product()