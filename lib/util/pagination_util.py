#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-28
@description:分页工具
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config import settings
from affiliate.lib.util.math_util import MathUtil


class Pagination(object):
    """
    分页对象

    """

    page_size = settings.page_size      #分页大小 默认为10

    page_current_number = 0             #当前页码

    page_prev_number = 0                #上一页页码

    page_next_number = 0                #下一页页码

    page_count = 0                      #总页数

    page_items = dict()                 #分页内容集合

    def __init__(self, page_items, items_count, **kwargs):
        page_number = int(kwargs.get('pageNumber'))
        page_size = int(kwargs.get('pageSize'))
        page_count = MathUtil.round(items_count, page_size)
        page_items = page_items
        self.pagination_support(page_number, page_size, page_count, page_items)

    def pagination_support(self, page_number, page_size, page_count, page_items):
        self.set_page_current_number(page_number)
        self.set_page_count(page_count)
        self.set_prev_page_number(page_number)
        self.set_next_page_number(page_number, page_count)
        self.set_page_size(page_size)
        self.set_page_items(page_items)

    def set_page_items(self, page_items):
        if isinstance(page_items, list):
            self.page_items = page_items

    def set_page_count(self, page_count):
        if page_count > 0:
            self.page_count = page_count

    def set_page_current_number(self, page_number):
        if page_number > 0:
            self.page_current_number = page_number

    def set_prev_page_number(self, page_number):
        if page_number > 1:
            self.page_prev_number = page_number - 1

    def set_page_size(self, page_size):
        if page_size > 0:
            self.page_size = page_size

    def set_next_page_number(self, page_number, page_count):
        if page_number < page_count:
            self.page_next_number = page_number + 1

    def __str__(self):
        return 'page_items:%s\npage_count:%s\npage_prev_number:%s\npage_current_number:%s\npage_next_nu' \
               'mber:%s\npage_size:%s' % (self.page_items, self.page_count, self.page_prev_number,
                                          self.page_current_number, self.page_next_number, self.page_size)










