#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-16
@description:测试导入商品列表
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config import settings

from affiliate.task.import_product import import_product_from_xml, import_product_image


def test_import_product(file_path):
    """
    测试导入商品列表

    """
    import_product_from_xml(file_path, settings.tag_dict)


def test_import_image(file_path):
    """
    测试导入商品列表

    """
    import_product_image(file_path, settings.tag_dict)


if __name__ == '__main__':
    file_path = 'D:/shopbot_en_2014_01_09.xml'
    test_import_product(file_path)