#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-6
@description:导出关键词
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.lib.util.file_util import FileUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def export_keyword(file_path, file_name):
    """导出关键词"""
    try:
        keyword_index_list = MongodbUtil.find('shopping', 'keywordIndex')
        file_content = ''
        index = 0
        for keyword_index in keyword_index_list:
            keyword = keyword_index.get('keyword')
            if index == 10:
                file_content = str(file_content) + ', ' + str(keyword) + '\n'
                index = 0
                continue
            file_content = str(file_content) + ', ' + str(keyword)
            index += 1
        FileUtil.write_2_file(file_path, file_name, file_content, 'utf-8')
    except Exception as e:
        logger.error(e.message)
