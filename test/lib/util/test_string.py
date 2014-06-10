#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-2-21
@description:字符工具模块测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def test_get_keyword_set(keyword):
    """获取关键字无重复集合"""
    keyword_set = list()
    #分词模板
    glossary = MongodbUtil.find_one('shopping', 'glossary')
    use_word_list = glossary.get('used')
    un_used_word_list = glossary.get('unUsed')
    for word in use_word_list:
        if keyword.__contains__(word):
            keyword_set.append(word)
    for word in StringUtil.cut_word(keyword):
        if not un_used_word_list.__contains__(word) and not keyword_set.__contains__(word):
            keyword_set.append(word)
    print keyword_set


def test_cut_word(word):
    result = StringUtil.cut_word(word)
    print result


if __name__ == '__main__':
    word = 'case+ipad+apple+case+apple'
    test_get_keyword_set(word)
    test_cut_word(word)