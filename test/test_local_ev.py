#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-2-17
@description:初始化本地数据库
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config import settings
from affiliate.lib.model.mongod.mongo_init import init_index
from affiliate.test.task.test_glossary import test_import_glossary
from affiliate.test.task.test_merchant import test_import_merchant
from affiliate.test.task.test_import_category import test_import_category
from affiliate.test.task.test_import_product import import_product_from_xml


def init_local_db(db):
    """初始化本地数据库"""
    if db == 'shopping':
        init_index(db)
        test_import_category()
        test_import_glossary()
        test_import_merchant('FocalPrice')
        import_product_from_xml('D:/shopbot_1.xml', settings.tag_dict)
    elif db == 'api':
        init_index(db)


if __name__ == '__main__':
    init_local_db('shopping')