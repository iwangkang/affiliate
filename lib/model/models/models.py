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

    def to_json(self):
        data = {
            'Status Code': 200,
            'Message': 'Successful operation!!!',
        }
        return json.dumps(data)


class PageResponse(ResponseBase):
    """
    产品分页响应

    """
    def __init__(self, product_id_list, **kwargs):
        try:
            self._webmaster_id = kwargs.get('webmasterId')
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
        return page_count

    def __get_page_items(self):
        """排序过滤product"""
        page_items = list()
        product_index = (self._page_index - 1) * self._page_size
        for p_id in self._product_id_list:
            product = MongodbUtil.find_one('product', str(p_id).encode('utf-8'))
            product = self.__filter_product(product)
            page_items.append(product)
            if page_items.__len__() == (self._page_index * self._page_size):
                return page_items[product_index:]
        return page_items

    def __filter_product(self, product):
        """参数处理"""
        del_key_list = ['keywordList', '_id']
        image_size = settings.image_size_list.get('small')
        image = MongodbUtil.find_one('image', {'imageProductId': product['_id'], 'imageWidth': image_size[0],
                                               'imageHeight': image_size[1]})
        if image:
            product['imageUrl'] = '%s/image?filename=%s' % (settings.host_src, image.get('fileName'))
        product['productMerchantId'] = product['productMerchantId'].__str__()
        if self._webmaster_id:
            product['productUrl'] = '%s/product?source=%s&productId=%s' % (settings.host_src, self._webmaster_id, product['_id'].__str__())
        else:
            del del_key_list[0]
            del product['productUrl']
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
