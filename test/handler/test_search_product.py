#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-2
@description:测试产品搜索handler
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import urllib2

from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.util.order_util import OrderUtil
from affiliate.lib.util.file_util import FileUtil
from affiliate.lib.model.pool.thread_pool import MyThreadPool
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def get_product_id_list(keyword):
    """从mongodb中获取产品id结果集"""
    keyword = keyword.lower()
    keyword_set = get_keyword_set(keyword)
    p_id_list_arr = list()
    union_dict = {}
    #按照分词结果查询产品结果集
    for i in xrange(len(keyword_set)):
        keyword_index = MongodbUtil.find_one('keywordIndex', {'keyword': keyword_set[i]})
        p_id_dict = keyword_index.get('invertedIndex')
        if p_id_dict:
            union_dict = dict(union_dict.items() + p_id_dict.items())
            p_id_list = sorted(p_id_dict, key=p_id_dict.get, reverse=True)
            p_id_list_arr.append(p_id_list)
    #结果集排序：先取交集，再取并集(取差集)，分别按照优先级排序，最后合并
    intersection = None
    union_set = None
    for i in xrange(len(p_id_list_arr)):
        if not intersection:
            intersection = p_id_list_arr[i]
            union_set = p_id_list_arr[i]
            continue
        intersection = list(set(intersection).intersection(set(p_id_list_arr[i])))
        union_set = list(set(union_set).union(set(p_id_list_arr[i])))
    union_set = list(set(union_set).difference(set(intersection)))
    #排序
    intersection = OrderUtil.order_obj_list(union_dict, intersection)
    union_set = OrderUtil.order_obj_list(union_dict, union_set)

    product_id_list = list()
    for i in xrange(len(intersection)):
        product_id_list.append(intersection[i])
    for i in xrange(len(union_set)):
        product_id_list.append(union_set[i])
    return product_id_list


def get_keyword_set(keyword):
    """获取关键字无重复集合"""
    keyword_set = list()
    #分词模板
    glossary = MongodbUtil.find_one('glossary')
    use_word_list = glossary.get('used')
    un_used_word_list = glossary.get('unUsed')
    for word in use_word_list:
        if keyword.__contains__(word):
            keyword_set.append(word)
    for word in StringUtil.cut_word(keyword):
        if not un_used_word_list.__contains__(word) and not keyword_set.__contains__(word):
            keyword_set.append(word)
    return keyword_set


def test_single_request(keyword, pageIndex):
    """单个搜索请求"""
    url = 'http://affiliate.xingcloud.com/product/search?webmasterId=123456&keyword=%s&pageSize=5&pageIndex=%s'\
          % (urllib2.quote(keyword), pageIndex)
    print(url)
    result = urllib2.urlopen(url)
    print result


def test_concurrent_request(keyword):
    """压力测试"""
    product_pool = MyThreadPool(num_threads=167, min_pool=69, max_pool=512)
    for i in xrange(1000000):
        pageIndex = random.randint(1, 167)
        product_pool.add_task(test_single_request, keyword, pageIndex)
    product_pool.wait_completion()


def test_keyword_search(file_path):
    """关键词查询测试"""
    search_pool = MyThreadPool(num_threads=96, min_pool=69, max_pool=128)
    # search_pool = MyThreadPool(num_threads=1, min_pool=1, max_pool=1)
    lines = FileUtil.read_file_lines_content(file_path, 'utf-8')
    for line in lines:
        keyword_list = line.split(',')
        for keyword in keyword_list:
            if not keyword:
                continue
            keyword = str(keyword).lstrip().rstrip().replace('\n', '').encode('utf-8')
            search_pool.add_task(test_single_request, keyword, 1)
    search_pool.wait_completion()


if __name__ == '__main__':
    test_keyword_search('D:\keyword_2014_01_09.txt')
    # keyword = 'Apple Accessories'
    # test_concurrent_request(keyword)