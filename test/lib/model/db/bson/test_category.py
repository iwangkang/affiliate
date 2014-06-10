#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-4-10
@description: 商品类别测试
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os

from affiliate.lib.util.xml_util import XMLUtil
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.util.file_util import FileUtil
from affiliate.lib.model.db.bson.category import category_dict


def test_add_keyword():
    """把已有的分类"""
    result_list = category_dict
    file_path = 'D:/xincloud/task_list/task_affiliate/feeds_demo/focalprice/FocalPrice_demo.xml'
    tag_name = 'product'
    product_list = XMLUtil.read_2_list(file_path, tag_name)
    for product in product_list:
        name = product.get('name')
        description = product.get('description')
        category = product.get('category')
        category_result = fit_category(result_list, category, name, description)
        result_list = fill_category_dict(result_list, category_result, category, name, description)
    file_path = FileUtil.write_2_file('D:/', 'category.txt', result_list, 'utf-8')
    print file_path


def fill_category_dict(result_list, category_result, category, name, description):
    """补充类别关键词"""
    c_k = result_list[category_result].get('category_keyword')
    d_k = result_list[category_result].get('desc_keyword')
    n_k = result_list[category_result].get('name_keyword')
    c_k_list = StringUtil.cut_word(category)
    d_k_list = StringUtil.cut_word(description)
    n_k_list = StringUtil.cut_word(name)
    for keyword in c_k_list:
        if not c_k.__contains__(keyword):
            c_k.append(keyword)
        if d_k.__contains__(keyword):
            d_k.remove(keyword)
        if n_k.__contains__(keyword):
            n_k.remove(keyword)
    for keyword in d_k_list:
        if not d_k.__contains__(keyword) and not c_k.__contains__(keyword):
            d_k.append(keyword)
        if n_k.__contains__(keyword):
            n_k.remove(keyword)
    for keyword in n_k_list:
        if not n_k.__contains__(keyword) and not d_k.__contains__(keyword) and not c_k.__contains__(keyword):
            n_k.append(keyword)
    result_list[category_result]['category_keyword'] = c_k
    result_list[category_result]['desc_keyword'] = d_k
    result_list[category_result]['name_keyword'] = n_k
    return result_list


def fit_category(result_list, category, name, description):
    """根据类别关键词定类"""
    percentage = 0.0
    category_result = 'Others'
    category_keyword_list = StringUtil.cut_word(category)
    name_keyword_list = StringUtil.cut_word(name)
    desc_keyword_list = StringUtil.cut_word(description)
    total_count = len(category_keyword_list) + len(name_keyword_list) + len(desc_keyword_list)
    for c, k_dict in result_list.items():
        grade = 0.0
        for keyword in category_keyword_list:
            if k_dict['category_keyword'].__contains__(keyword):
                grade += 3.0
        for keyword in name_keyword_list:
            if k_dict['desc_keyword'].__contains__(keyword):
                grade += 0.1
        for keyword in desc_keyword_list:
            if k_dict['name_keyword'].__contains__(keyword):
                grade += 0.05

        new_percentage = float(grade) / float(total_count)
        if percentage < new_percentage:
            category_result = c
            percentage = new_percentage
    return category_result


def test_get_single_keyword(result_set, file_path):
    """把已有的分类"""
    tag_name = 'product'
    product_list = XMLUtil.read_2_list(file_path, tag_name)
    for product in product_list:
        category = product.get('category')
        name = product.get('name')
        description = product.get('description')
        category_keyword_list = StringUtil.cut_word(category)
        name_keyword_list = StringUtil.cut_word(name)
        desc_keyword_list = StringUtil.cut_word(description)
        category_keyword_list.extend(name_keyword_list)
        for keyword in desc_keyword_list:
            if keyword not in category_keyword_list:
                result_set.add(keyword)
    return result_set

def test_get_filename_list(path):
    """获取文件夹下所有文件名"""
    for root, dirs, files in os.walk(dir):
        for f in files:
            print type(f)


if __name__ == '__main__':
    result_set = set()
    for index in range(21):
        index += 1
        file_path = 'D:/xincloud/task_list/task_affiliate/feeds_demo/honeybuy/Dresses_HoneyBuy/%s.xml' % index
        result_set = test_get_single_keyword(result_set, file_path)
    print list(result_set)