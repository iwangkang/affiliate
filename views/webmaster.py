#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-25
@description:广告跟踪统计模块
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config import settings
from affiliate.views.base import BaseHandler
from affiliate.lib.util.logger_util import logger
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.util.order_util import OrderUtil
from affiliate.lib.model.cache.memcache_win import McCache
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil
from affiliate.lib.model.models.models import PageResponse, BrokenResponse


class SearchProductHandler(BaseHandler):
    """
    产品搜索

    """

    def on_request(self):
        try:
            #查询数据
            page_response = self.search_product(**self.params)
            #以json形式返回数据
            self._jsonify_response(page_response)
        except Exception as e:
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))
            error_response = BrokenResponse()
            self._jsonify_response(error_response)

    def search_product(self, **kwargs):
        """
        查询产品列表

        """
        self._event('list')
        #先从缓存取，缓存没有再去数据库
        mc = McCache()
        cache_key = StringUtil.str2md5('%s-%s-%s-%s' % (kwargs.get('webmasterId'), kwargs.get('keyword'),
                                                        kwargs.get('pageSize'), kwargs.get('pageIndex')))
        page_response = mc.get_obj(cache_key)
        if not page_response:
            self._event('not cache')
            product_id_list = self.get_product_id_list(**kwargs)
            page_response = PageResponse(product_id_list, **kwargs)
            mc.put_obj(cache_key, page_response, settings.search_timeout)
        return page_response

    def get_product_id_list(self, **kwargs):
        """从mongodb中获取产品id结果集"""
        keyword = kwargs.get('keyword').lower()
        keyword_set = self.get_keyword_set(keyword)
        p_id_list_arr = list()
        union_dict = {}
        #按照分词结果查询产品结果集
        for i in xrange(len(keyword_set)):
            keyword_index = MongodbUtil.find_one('keywordIndex', {'keyword': keyword_set[i]})
            if not keyword_index:
                continue
            p_id_dict = keyword_index.get('invertedIndex')
            if p_id_dict:
                union_dict = dict(union_dict.items() + p_id_dict.items())
                p_id_list = sorted(p_id_dict, key=p_id_dict.get, reverse=True)
                p_id_list_arr.append(p_id_list)
        #结果集排序：先取交集，再取并集(取差集)，分别按照优先级排序，最后合并
        intersection = list()
        union_set = list()
        for i in xrange(len(p_id_list_arr)):
            if not intersection:
                intersection = p_id_list_arr[i]
                union_set = p_id_list_arr[i]
                continue
            intersection = list(set(intersection).intersection(set(p_id_list_arr[i])))
            union_set = list(set(union_set).union(set(p_id_list_arr[i])))
        if intersection and union_set:
            union_set = list(set(union_set).difference(set(intersection)))
        #排序
        if intersection:
            intersection = OrderUtil.order_obj_list(union_dict, intersection)
        if union_set:
            union_set = OrderUtil.order_obj_list(union_dict, union_set)

        product_id_list = list()
        for i in xrange(len(intersection)):
            product_id_list.append(intersection[i])
        for i in xrange(len(union_set)):
            product_id_list.append(union_set[i])
        return product_id_list

    def get_keyword_set(self, keyword):
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


class CPCHandler(BaseHandler):
    """
    CPC数据跟踪统计

    """

    def on_request(self):
        try:
            redirect_url = self.cpc_effect(**self.params)
            if not redirect_url:
                self.redirect(url=settings.host_src, permanent=True)
            self.redirect(url=redirect_url, permanent=True)
        except Exception as e:
            self.cpc_un_effect(**self.params)
            self.redirect(url=settings.host_src, permanent=True)
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))

    def cpc_un_effect(self, **kwargs):
        """浏览器异常关闭有效点击数减一"""
        self._event('cpc_un_effect')
        product_id = kwargs.get('productId').encode('utf-8')
        exist_product = MongodbUtil.find_one('product', product_id)
        if exist_product:
            spec_or_id = {
                'from': kwargs.get('source'),
                'to': exist_product.get('productMerchantId'),
                'cpcProductId': exist_product.get('_id'),
            }
            document = {'$inc': {'cpcActiveCount': -1}}
            update_result = MongodbUtil.update('cpc', spec_or_id, document)

            if not update_result.get('updatedExisting'):
                self.cpc_un_effect(**kwargs)
            logger.info('Subtract an active click.')

    def cpc_effect(self, **kwargs):
        """更新点击数及有效点击数"""
        self._event('cpc_effect')
        product_id = kwargs.get('productId').encode('utf-8')
        exist_product = MongodbUtil.find_one('product', product_id)
        if exist_product:
            update_flag = self.add_cpc(exist_product, **kwargs)
            if not update_flag:
                self.insert_cpc(exist_product, **kwargs)
            logger.info('Add a click and an active click.')
            return exist_product.get('productUrl')
        else:
            return None

    def add_cpc(self, product, **kwargs):
        """点击数加一"""
        spec_or_id = {
            'from': kwargs.get('source'),
            'to': product.get('productMerchantId'),
            'cpcProductId': product.get('_id'),
        }
        document = {'$inc': {'cpcCount': 1, 'cpcActiveCount': 1}}
        update_result = MongodbUtil.update('cpc', spec_or_id, document)
        update_flag = update_result.get('updatedExisting')
        return update_flag

    def insert_cpc(self, product, **kwargs):
        """插入新增点击"""
        cpc_document = {
            'from': kwargs.get('source'),
            'to': product.get('productMerchantId'),
            'cpcCount': 1,
            'cpcActiveCount': 1,
            'cpcProductId': product.get('_id'),
        }
        MongodbUtil.insert('cpc', cpc_document)


class ImageHandler(BaseHandler):
    """
    图片加载

    """

    def on_request(self):
        try:
            self.load_image(**self.params)
        except Exception as e:
            self.redirect(url=settings.host_src, permanent=True)
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))

    def load_image(self, **kwargs):
        """根据文件名从mongdb中取出图片"""
        self._event('image')
        file_name = kwargs.get('filename')
        image_dict = MongodbUtil.get(filename=file_name)
        if not image_dict:
            self.redirect(url=settings.host_src, permanent=True)
            self.finish()
            return
        else:
            for k, v in image_dict.get('headers').items():
                self.set_header(k, v)
            self.write(image_dict.get('file'))
            self.finish()