#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-3-14
@description:初始化线上数据库  注意：执行前需要在添加环境变量export AFFILIATE_ENV='production'
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.lib.model.mongod.mongo_init import init_index
from affiliate.test.task.test_glossary import test_import_glossary
from affiliate.test.task.test_import_category import test_import_category


def init_local_db(db):
    """初始化本地数据库"""
    if db == 'shopping':
        init_index(db)
        test_import_category()
        test_import_glossary()
    elif db == 'api':
        init_index(db)


if __name__ == '__main__':
    init_local_db('api')
