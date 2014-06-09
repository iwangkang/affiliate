#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-30
@description:导入词汇表
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.lib.util.xml_util import XMLUtil
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.model.db.bson.glossary import glossary
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def import_glossary():
    """导入基础词汇表"""
    try:
        exists_glossary = MongodbUtil.find_one('glossary')
        if exists_glossary:
            message = 'The glossary is exists!!!'
            logger.info(message)
            return
        id = MongodbUtil.insert('glossary', glossary)
        if id:
            message = 'Import glossary(id:%s) successfully!!!' % id
            logger.info(message)
    except Exception as e:
        logger.error(e.message)


def replenish_glossary(file_path, tag_name, obj_id=None):
    """根据文件补充词汇表"""
    try:
        glossary = MongodbUtil.find_one('glossary', obj_id)
        category_list = XMLUtil.read_2_list(file_path, tag_name)
        category_set = XMLUtil.get_obj_set(category_list)
        for category in category_set:
            clean_word_list = StringUtil.clean_list(category.get(tag_name).split(':'))
            for word in clean_word_list.__iter__():
                word = word.lower()
                if not glossary.get('used').__contains__(word):
                    glossary.get('used').append(word)
        id = MongodbUtil.save('glossary', glossary)
        if id:
            message = 'Replenish glossary(id:%s) successfully!!!' % id
            logger.info(message)
    except Exception as e:
        logger.error(e.message)