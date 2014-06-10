#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-3-14
@description:测试导入类别词汇表
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.import_category import import_category


def test_import_category():
    import_category()


if __name__ == '__main__':
    #导入glossary
    test_import_category()