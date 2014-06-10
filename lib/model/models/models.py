#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-17
@description:接口请求模型
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import abc
import ujson as json

from affiliate.config import settings
from affiliate.lib.util.logger_util import logger
from affiliate.lib.util.math_util import MathUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


class ResponseBase(object):
    """
    接口响应抽象类

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_json(self):
        pass


class BrokenResponse(ResponseBase):
    """
    友善错误响应

    """

    def to_json(self):
        data = {
            'Status Code': 404,
            'Message': 'An unknown error has occurred, please check your request. We express our deep apologies',
        }
        return json.dumps(data)


class SuccessfulResponse(ResponseBase):
    """
    成功响应

    """

    def __init__(self, message=None):
        self._message = message

    def to_json(self):
        if self._message:
            data = {
                'Status Code': 200,
                'Message': self._message,
            }
        else:
            data = {
                'Status Code': 200,
                'Message': 'Successful operation!!!',
            }
        return json.dumps(data)


class HotWordResponse(ResponseBase):
    """
    热词数据响应

    """

    def __init__(self, keyword):
        try:
            self._hot_word_list = self._get_hot_word_list(keyword)
        except Exception as e:
            logger.error('Get hot word list response error.')

    def _get_hot_word_list(self, keyword):
        """获取热词列表"""
        hot_word_list = list()
        keyword_index_list = MongodbUtil.find('shopping', 'keywordIndex', spec_or_id={'keyword': {'$regex': keyword}}, skip=0,
                                              limit=10, sort=[(u'searchTimes', -1)])
        for keyword_index in keyword_index_list:
            keyword = keyword_index.get('keyword')
            if hot_word_list.__contains__(keyword):
                continue
            hot_word_list.append(keyword)
        return hot_word_list

    def to_json(self):
        return json.dumps(self._hot_word_list)


class PageResponse(ResponseBase):
    """
    监测数据分页对象

    """

    def __init__(self, page_index, page_size, page_count, page_items):
        try:
            self._page_index = page_index
            self._page_size = page_size
            self._page_count = page_count
            self._page_items = page_items
        except (KeyError, TypeError, ValueError, AssertionError) as e:
            logger.error('Get a page response error.')

    def to_json(self):
        data = {
            'pageIndex': self._page_index,
            'pageSize': len(self._page_items),
            'pageCount': self._page_count,
            'pageItems': [product_cpc for product_cpc in self._page_items],
        }
        return json.dumps(data)


class ProductPageResponse(ResponseBase):
    """
    产品分页响应

    """

    def __init__(self, product_id_list, **kwargs):
        try:
            self._webmaster = kwargs.get('webmaster')
            self._product_id_list = product_id_list or list()
            self._page_size = int(kwargs.get('pageSize', settings.page_size))
            self._page_index = int(kwargs.get('pageIndex', 1))
            self._page_count = self.__get_page_count()
            self._page_items = self.__get_page_items()
        except (KeyError, TypeError, ValueError, AssertionError) as e:
            logger.error('Get a page response error.')

    def __get_page_count(self):
        """计算页码总数"""
        product_count = 0
        product_count += len(self._product_id_list)
        page_count = MathUtil.round(product_count, self._page_size)
        if page_count == 0:
            page_count = 1
        return page_count

    def __get_page_items(self):
        """排序过滤product, 获取产品列表"""
        page_items = list()
        begin_index = (self._page_index - 1) * self._page_size
        end_index = self._page_index * self._page_size
        product_id_list = self._product_id_list[begin_index: end_index]
        for p_id in product_id_list:
            product = MongodbUtil.find_one('shopping', 'product', str(p_id).encode('utf-8'))
            product = self.__filter_product(product)
            page_items.append(product)
        return page_items

    def __filter_product(self, product):
        """参数处理"""
        del_key_list = ['keywordList', '_id', 'merchantId', 'sellTotalCount']
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'_id': product.get('merchantId')})
        product['merchant'] = merchant.get('name')
        if self._webmaster:
            product['url'] = '%s/cpc?s=%s&p_i=%s&a_p_i=' % (
            settings.host_src, self._webmaster, product['_id'].__str__())
            image_arr = MongodbUtil.find('shopping', 'image', {'productId': product['_id']})
            if image_arr and len(image_arr) == 3:
                product['smallImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[0].get('fileName'))
                product['middleImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[1].get('fileName'))
                product['bigImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[2].get('fileName'))
            else:
                product['smallImageUrl'] = settings.default_product_pic
                product['middleImageUrl'] = settings.default_product_pic
                product['bigImageUrl'] = settings.default_product_pic
        else:
            del del_key_list[del_key_list.index('keywordList')]
            del product['url']
        for k, v in product.items():
            if k in del_key_list:
                del product[k]
        return product

    def to_json(self):
        data = {
            'pageIndex': self._page_index,
            'pageSize': len(self._page_items),
            'pageCount': self._page_count,
            'pageItems': [product for product in self._page_items],
        }
        return json.dumps(data)

    def to_dict(self):
        page = {
            'pageIndex': self._page_index,
            'pageSize': len(self._page_items),
            'pageCount': self._page_count,
            'pageItems': [product for product in self._page_items],
        }
        return page


class SuggestResponse(ResponseBase):
    """
    商品推荐响应

    """

    def __init__(self, product_list, **kwargs):
        try:
            self._webmaster = kwargs.get('w_m')
            self._product_list = product_list
            self._page_items = self.__get_page_items()
        except (KeyError, TypeError, ValueError, AssertionError) as e:
            logger.error('Get a page response error.')

    def __get_page_items(self):
        """排序过滤product, 获取产品列表"""
        page_items = list()
        for product in self._product_list:
            product = self.__filter_product(product)
            page_items.append(product)
        return page_items

    def __filter_product(self, product):
        """参数处理"""
        del_key_list = ['keywordList', '_id', 'merchantId', 'sellTotalCount']
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'_id': product.get('merchantId')})
        product['merchant'] = merchant.get('name')
        if self._webmaster:
            product['url'] = '%s/cpc?s=%s&p_i=%s&a_p_i=' % (settings.host_src, self._webmaster, product['_id'].__str__())
            image_arr = MongodbUtil.find('shopping', 'image', {'productId': product['_id']})
            if image_arr and len(image_arr) == 3:
                product['smallImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[0].get('fileName'))
                product['middleImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[1].get('fileName'))
                product['bigImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[2].get('fileName'))
            else:
                product['smallImageUrl'] = settings.default_product_pic
                product['middleImageUrl'] = settings.default_product_pic
                product['bigImageUrl'] = settings.default_product_pic
        else:
            del del_key_list[del_key_list.index('keywordList')]
            del product['url']
        for k, v in product.items():
            if k in del_key_list:
                del product[k]
        return product

    def to_json(self):
        data = {
            'suggestItems': [product for product in self._page_items],
        }
        return json.dumps(data)

    def to_dict(self):
        page = {
            'suggestItems': [product for product in self._page_items],
        }
        return page


class ListPageResponse(ResponseBase):
    """
    shopping 列表页数据集

    """

    def __init__(self, product_list, **kwargs):
        try:
            self._webmaster = kwargs.get('webmaster')
            self._product_list = product_list
            self._page_size = int(kwargs.get('pageSize', settings.page_size))
            self._page_index = int(kwargs.get('pageIndex', 1))
            self._page_count = self.__get_page_count()
            self._page_items = self.__get_page_items()
        except (KeyError, TypeError, ValueError, AssertionError) as e:
            logger.error('Get a page response error.')

    def __get_page_count(self):
        """计算页码总数"""
        product_count = len(self._product_list)
        page_count = MathUtil.round(product_count, self._page_size)
        if page_count == 0:
            page_count = 1
        return page_count

    def __get_page_items(self):
        """排序过滤product, 获取产品列表"""
        page_items = list()
        begin_index = (self._page_index - 1) * self._page_size
        end_index = self._page_index * self._page_size
        product_list = self._product_list[begin_index: end_index]
        for product in product_list:
            product = self.__filter_product(product)
            page_items.append(product)
        return page_items

    def __filter_product(self, product):
        """参数处理"""
        del_key_list = ['keywordList', '_id', 'merchantId', 'sellTotalCount']
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'_id': product.get('merchantId')})
        product['merchant'] = merchant.get('name')
        if self._webmaster:
            product['url'] = '%s/cpc?s=%s&p_i=%s&a_p_i=' % (
            settings.host_src, self._webmaster, product['_id'].__str__())
            image_arr = MongodbUtil.find('shopping', 'image', {'productId': product['_id']})
            if image_arr and len(image_arr) == 3:
                product['smallImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[0].get('fileName'))
                product['middleImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[1].get('fileName'))
                product['bigImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[2].get('fileName'))
            else:
                product['smallImageUrl'] = settings.default_product_pic
                product['middleImageUrl'] = settings.default_product_pic
                product['bigImageUrl'] = settings.default_product_pic
        else:
            del del_key_list[del_key_list.index('keywordList')]
            del product['url']
        for k, v in product.items():
            if k in del_key_list:
                del product[k]
        return product

    def to_json(self):
        data = {
            'pageIndex': self._page_index,
            'pageSize': len(self._page_items),
            'pageCount': self._page_count,
            'pageItems': [product for product in self._page_items],
        }
        return json.dumps(data)

    def to_dict(self):
        page = {
            'pageIndex': self._page_index,
            'pageSize': len(self._page_items),
            'pageCount': self._page_count,
            'pageItems': [product for product in self._page_items],
        }
        return page