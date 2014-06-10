#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-3-14
@description:导入类别集合
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from affiliate.task.base import *
from affiliate.lib.model.db.bson.category import category_dict
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def import_category():
    """导入基础词汇表"""
    try:
        exists_category = MongodbUtil.find_one('shopping', 'category')
        if exists_category:
            message = 'The category is exists!!!'
            logger.info(message)
            return
        id = MongodbUtil.insert('shopping', 'category', category_dict)
        if id:
            message = 'Import category(id:%s) successfully!!!' % id
            logger.info(message)
    except Exception as e:
        logger.error(e.message)


if __name__ == '__main__':
    pass