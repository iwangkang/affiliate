#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-8-19
@description:网盟shopping模块业务逻辑层，处理请求业务逻辑
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import ast
import random

from affiliate.config import settings
from affiliate.config.celeryconfig import affiliate_celery
from affiliate.views.base import BaseHandler
from affiliate.task.import_product import do_import_product
from affiliate.task.import_merchant import import_merchant, import_product_id_2_merchant
from affiliate.lib.util.logger_util import logger
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.util.xml_util import XMLUtil
from affiliate.lib.util.check_util import CheckUtil
from affiliate.lib.util.file_util import FileUtil
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.util.order_util import OrderUtil
from affiliate.lib.model.db.bson.category import category_name_map
from affiliate.lib.model.cache.memcache_win import McCache
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil
from affiliate.lib.model.models.models import ListPageResponse, HotWordResponse, ProductPageResponse, BrokenResponse, SuccessfulResponse


class IndexHandler(BaseHandler):
    """
    首页

    """

    def get(self):
        try:
            self._event('index')
            mc = McCache()
            cache_key = StringUtil.str2md5('shopping-index')
            product_arr = mc.get_obj(cache_key)
            if not product_arr:
                self._event('not_cache')
                product_arr = self._get_index_product_arr()
                if product_arr:
                    mc.put_obj(cache_key, product_arr, settings.index_timeout)
                    self.render(settings.index_template, product_arr=product_arr)
                else:
                    self._event('error')
                    self.render(settings.error_template)
            else:
                self._event('cache')
                self.render(settings.index_template, product_arr=product_arr)
        except Exception as e:
            logger.error('[message: %s]' % e.message)
            self.render(settings.error_template)

    def _get_merchant_list(self):
        """
        获取广告主列表

        """
        merchant_name_list = list()
        merchant_list = MongodbUtil.find('shopping', 'merchant')
        for merchant in merchant_list:
            merchant_name_list.append(merchant.get('name'))
        return merchant_name_list

    def _get_index_product_arr(self):
        """随机筛选首页展示产品集合"""
        temp_category_name_map = dict(category_name_map)
        keys_list = temp_category_name_map.keys()
        first_key = keys_list[random.randint(0, len(keys_list) - 1)]
        second_key = keys_list[random.randint(0, len(keys_list) - 1)]
        first_products = MongodbUtil.find('shopping', 'product', spec_or_id={'category': temp_category_name_map.pop(first_key)}, skip=0, limit=12, sort=[(u'startTime', -1)])
        while len(first_products) < 12 and len(temp_category_name_map) != 0:
            keys_list = temp_category_name_map.keys()
            first_key = keys_list[random.randint(0, len(keys_list))]
            first_products = MongodbUtil.find('shopping', 'product', spec_or_id={'category': temp_category_name_map.pop(first_key)}, skip=0, limit=12, sort=[(u'startTime', -1)])
        second_products = MongodbUtil.find('shopping', 'product', spec_or_id={'category': temp_category_name_map.pop(second_key)}, skip=0, limit=12, sort=[(u'startTime', -1)])
        while len(second_products) < 12 and len(temp_category_name_map) != 0:
            keys_list = temp_category_name_map.keys()
            second_key = keys_list[random.randint(0, len(keys_list))]
            second_products = MongodbUtil.find('shopping', 'product', spec_or_id={'category': temp_category_name_map.pop(second_key)}, skip=0, limit=12, sort=[(u'startTime', -1)])
        if len(first_products) == 0 or len(second_products) == 0:
            return None
        first_product_list = self.assemble_product_info(first_products)
        second_product_list = self.assemble_product_info(second_products)
        product_arr = {
            'first': {
                'category': category_name_map.get(first_key),
                'productList': first_product_list
            },
            'second': {
                'category': category_name_map.get(second_key),
                'productList': second_product_list
            }
        }
        return product_arr

    def assemble_product_info(self, products):
        product_list = list()
        for p in products:
            merchant = MongodbUtil.find_one('shopping', 'merchant', spec_or_id={'_id': p.get('merchantId')})
            product = {
                "productId": p.get('productId'),
                "title": p.get('title'),
                "merchant": merchant.get('name'),
                "price": p.get('price'),
                "currency": p.get('currency'),
                "mpn": p.get('mpn'),
                "aliveTime": p.get('aliveTime'),
                "startTime": p.get('startTime'),
                "description": str(p.get('description')),
            }
            image_arr = MongodbUtil.find('shopping', 'image', {'productId': p['_id']})
            if image_arr and len(image_arr) == 3:
                product['smallImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[0].get('fileName'))
                product['middleImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[1].get('fileName'))
                product['bigImageUrl'] = '%s/image?filename=%s' % (settings.host_src, image_arr[2].get('fileName'))
            else:
                product['smallImageUrl'] = settings.default_product_pic
                product['middleImageUrl'] = settings.default_product_pic
                product['bigImageUrl'] = settings.default_product_pic
            product['url'] = '%s/cpc?s=%s&p_i=%s&a_p_i=' % (settings.host_src, settings.webmaster, p.get('_id').__str__())
            product_list.append(product)
        return product_list


class IndexListHandler(BaseHandler):
    """
    列表页

    """

    def get(self):
        try:
            page = self.search_product(**self.params)
            if len(page.get('pageItems')) != 0:
                if page['list_type'] == 'w_v':
                    self.render(settings.web_view_template, page=page)
                elif page['list_type'] == 'l_v':
                    self.render(settings.list_view_template, page=page)
                else:
                    self.render(settings.error_template)
            else:
                keyword = self.params.get('keyword').rstrip().lstrip().lower()
                if keyword:
                    suggest_keyword = self._get_suggest_keyword(keyword)
                    page['suggestKeyword'] = suggest_keyword
                else:
                    page['suggestKeyword'] = ''
                self.render(settings.nothing_template, page=page)
        except Exception as e:
            self.render(settings.error_template)
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))

    def post(self):
        try:
            page = self.search_product(**self.params)
            if len(page.get('pageItems')) != 0:
                if page['list_type'] == 'w_v':
                    self.render(settings.web_view_template, page=page)
                elif page['list_type'] == 'l_v':
                    self.render(settings.list_view_template, page=page)
                else:
                    self.render(settings.error_template)
            else:
                keyword = self.params.get('keyword').rstrip().lstrip().lower()
                if keyword:
                    suggest_keyword = self._get_suggest_keyword(keyword)
                    page['suggestKeyword'] = suggest_keyword
                else:
                    page['suggestKeyword'] = ''
                self.render(settings.nothing_template, page=page)
        except Exception as e:
            keyword = self.params.get('keyword').lstrip().rstrip()
            self.render(settings.error_template)
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))

    def _get_suggest_keyword(self, keyword):
        """获取建议词汇"""
        suggest_keyword = ''
        keyword_index = MongodbUtil.find('shopping', 'keywordIndex', spec_or_id={'keyword': {'$regex': keyword}},
                                         skip=0, limit=1,
                                         sort=[(u'searchTimes', -1)])
        if keyword_index:
            suggest_keyword = keyword_index[0].get('keyword')
        return suggest_keyword

    def search_product(self, **kwargs):
        """
        查询产品列表

        """
        self._event('list_page')
        #查询参数校验
        if not self._check_params(**self.params):
            self._event('check_false')
            page = self._get_default_page(**self.params)
            return page
            #先从缓存取，缓存没有再去数据库
        mc = McCache()
        cache_key = StringUtil.str2md5('shopping-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s-%s' %
                                       (kwargs.get('webmaster'), kwargs.get('keyword', 'keyword'),
                                        kwargs.get('c_k', 'c_k'), kwargs.get('pageSize'), kwargs.get('pageIndex'),
                                        kwargs.get('p_s'), kwargs.get('l_t'), kwargs.get('f_n'),
                                        kwargs.get('l_p', 'l_p'),
                                        kwargs.get('u_p', 'u_p'), kwargs.get('m_n', 'm_n')))
        page = mc.get_obj(cache_key)
        if not page:
            page = self._get_product_list(mc, cache_key, **kwargs)
        else:
            keyword = kwargs.get('keyword').lstrip().rstrip()
            if keyword:
                self._add_search_times(keyword)

        page = self._assemble_page(page, **kwargs)
        return page

    def _assemble_page(self, page, **kwargs):
        """拼装商品参数列表"""
        merchant_list = self._get_merchant_list(kwargs.get('m_n'))
        page['category_keyword'] = kwargs.get('c_k')
        page['price_sort'] = kwargs.get('p_s')
        page['keyword'] = kwargs.get('keyword')
        page['list_type'] = kwargs.get('l_t')
        page['filter_price'] = self._filter_price(**kwargs)
        page['filter_new'] = kwargs.get('f_n')
        page['merchant_name'] = kwargs.get('m_n')
        page['show_merchant_list'] = merchant_list[0:5] or list()
        page['hidden_merchant_list'] = merchant_list[5:] or list()
        return page

    def _filter_price(self, **kwargs):
        """获取价格筛选参数"""
        filter_price = dict()
        if kwargs.get('l_p') and kwargs.get('u_p'):
            filter_price['description'] = str(kwargs.get('l_p')) + ' - ' + (kwargs.get('u_p'))
            filter_price['lower_price'] = kwargs.get('l_p')
            filter_price['upper_price'] = kwargs.get('u_p')
        elif not kwargs.get('l_p') and kwargs.get('u_p'):
            filter_price['description'] = 'Less then ' + (kwargs.get('u_p'))
            filter_price['lower_price'] = ''
            filter_price['upper_price'] = kwargs.get('u_p')
        elif kwargs.get('l_p') and not kwargs.get('u_p'):
            filter_price['description'] = 'More then ' + str(kwargs.get('l_p'))
            filter_price['lower_price'] = kwargs.get('l_p')
            filter_price['upper_price'] = ''
        else:
            filter_price = None
        return filter_price

    def _get_default_page(self, **kwargs):
        """返回默认的空page"""
        merchant_name = kwargs.get('m_n')
        merchant_list = self._get_merchant_list(merchant_name)
        page = {
            'category_keyword': kwargs.get('c_k'),
            'price_sort': kwargs.get('p_s'),
            'keyword': kwargs.get('keyword'),
            'list_type': kwargs.get('l_t'),
            'filter_price': None,
            'filter_new': kwargs.get('f_n'),
            'merchant_name': kwargs.get('m_n'),
            'show_merchant_list': merchant_list[0:5] or list(),
            'hidden_merchant_list': merchant_list[5:] or list(),
            'pageIndex': 1,
            'pageSize': 0,
            'pageCount': 1,
            'pageItems': list(),
        }
        return page

    def _get_merchant_list(self, merchant_name):
        """将点击获取商户列表"""
        merchant_name_list = list()
        merchant_list = MongodbUtil.find('shopping', 'merchant')
        for merchant in merchant_list:
            merchant_name_list.append(merchant.get('name'))
        if not merchant_name or not (merchant_name_list.__contains__(merchant_name)):
            return merchant_name_list
        merchant_name_list.remove(merchant_name)
        merchant_name_list.append(merchant_name)
        merchant_name_list.reverse()
        return merchant_name_list

    def _get_product_list(self, mc, cache_key, **kwargs):
        """没有缓存搜索产品列表，搜索并存入缓存"""
        self._event('not cache')
        today = DateUtil.get_sys_date()
        category = category_name_map.get(kwargs.get('c_k'))
        price_section = self._get_price_section(str(kwargs.get('l_p')), str(kwargs.get('u_p')))
        merchant_id = None
        if kwargs.get('m_n'):
            merchant_id = self._get_merchant_id(kwargs.get('m_n'))
            if not merchant_id:
                page = {
                    'pageIndex': 1,
                    'pageSize': 60,
                    'pageCount': 1,
                    'pageItems': list(),
                }
                return page
        if category:
            if kwargs.get('p_s') == 'up':
                if kwargs.get('f_n') == 'checked':
                    if price_section:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today,
                                                                        'merchantId': merchant_id,
                                                                        '$where': price_section}, sort=[(u'price', 1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today,
                                                                        '$where': price_section}, sort=[(u'price', 1)])
                    else:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today,
                                                                        'merchantId': merchant_id},
                                                            sort=[(u'price', 1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today},
                                                            sort=[(u'price', 1)])
                elif kwargs.get('f_n') == 'unchecked':
                    if price_section:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'merchantId': merchant_id,
                                                                        '$where': price_section}, sort=[(u'price', 1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, '$where': price_section},
                                                            sort=[(u'price', 1)])
                    else:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category,
                                                                                               'merchantId': merchant_id},
                                                            sort=[(u'price', 1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category},
                                                            sort=[(u'price', 1)])

            elif kwargs.get('p_s') == 'down':
                if kwargs.get('f_n') == 'checked':
                    if price_section:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today,
                                                                        'merchantId': merchant_id,
                                                                        '$where': price_section}, sort=[(u'price', -1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today,
                                                                        '$where': price_section}, sort=[(u'price', -1)])
                    else:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today,
                                                                        'merchantId': merchant_id},
                                                            sort=[(u'price', -1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'startTime': today},
                                                            sort=[(u'price', -1)])
                elif kwargs.get('f_n') == 'unchecked':
                    if price_section:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, 'merchantId': merchant_id,
                                                                        '$where': price_section}, sort=[(u'price', -1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            spec_or_id={'category': category, '$where': price_section},
                                                            sort=[(u'price', -1)])
                    else:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category,
                                                                                               'merchantId': merchant_id},
                                                            sort=[(u'price', -1)])
                        else:
                            product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category},
                                                            sort=[(u'price', -1)])
            else:
                if kwargs.get('f_n') == 'checked':
                    if price_section:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, 'startTime': today,
                                                             'merchantId': merchant_id,
                                                             '$where': price_section})
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, 'startTime': today,
                                                             '$where': price_section})
                    else:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, 'startTime': today,
                                                             'merchantId': merchant_id})
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, 'startTime': today})
                elif kwargs.get('f_n') == 'unchecked':
                    if price_section:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, 'merchantId': merchant_id,
                                                             '$where': price_section})
                        else:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, '$where': price_section})
                    else:
                        if merchant_id:
                            product_list = MongodbUtil.find('shopping', 'product',
                                                            {'category': category, 'merchantId': merchant_id})
                        else:
                            product_list = MongodbUtil.find('shopping', 'product', {'category': category})
            page_response = ListPageResponse(product_list, **kwargs)
            page = page_response.to_dict()
            mc.put_obj(cache_key, page, settings.search_timeout)
        elif kwargs.get('keyword'):
            product_id_list = self.get_product_id_list(**kwargs)
            product_list = self._get_sort_list(merchant_id, product_id_list, **kwargs)
            page_response = ListPageResponse(product_list, **kwargs)
            page = page_response.to_dict()
            mc.put_obj(cache_key, page, settings.search_timeout)
        else:
            page = {
                'pageIndex': 1,
                'pageSize': 60,
                'pageCount': 1,
                'pageItems': list(),
            }
        return page

    def _get_merchant_id(self, merchant_name):
        """获取商户id"""
        merchant_id = None
        if not merchant_name:
            return merchant_id
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant_name})
        if merchant:
            merchant_id = merchant.get('_id')

        return merchant_id

    def _get_price_section(self, lower_price, upper_price):
        """获得根据价格区间筛选商品"""
        price_section = None
        if lower_price and upper_price:
            price_section = 'this.price > ' + str(lower_price) + ' & this.price < ' + str(upper_price)
        elif not lower_price and upper_price:
            price_section = 'this.price < ' + str(upper_price)
        elif lower_price and not upper_price:
            price_section = 'this.price > ' + str(lower_price)
        return price_section

    def _get_sort_list(self, merchant_id, product_id_list, **kwargs):
        """根据产品id集合过滤排序获取商品列表"""
        today = DateUtil.get_sys_date()
        product_list = list()
        for product_id in product_id_list:
            product = MongodbUtil.find_one('shopping', 'product', spec_or_id=str(product_id))
            if merchant_id and product.get('merchantId') != merchant_id:
                continue
            if kwargs.get('f_n') == 'checked':
                if product.get('startTime') == today:
                    if kwargs.get('l_p') and kwargs.get('u_p'):
                        if (float(product.get('price')) > float(kwargs.get('l_p'))) and \
                                (float(product.get('price')) < float(kwargs.get('u_p'))):
                            product_list.append(product)
                    elif not kwargs.get('l_p') and kwargs.get('u_p'):
                        if float(product.get('price')) < float(kwargs.get('u_p')):
                            product_list.append(product)
                    elif kwargs.get('l_p') and not kwargs.get('u_p'):
                        if float(product.get('price')) > float(kwargs.get('l_p')):
                            product_list.append(product)
                    else:
                        product_list.append(product)
            else:
                if kwargs.get('l_p') and kwargs.get('u_p'):
                    if (float(product.get('price')) > float(kwargs.get('l_p'))) and \
                            (float(product.get('price')) < float(kwargs.get('u_p'))):
                        product_list.append(product)
                elif not kwargs.get('l_p') and kwargs.get('u_p'):
                    if float(product.get('price')) < float(kwargs.get('u_p')):
                        product_list.append(product)
                elif kwargs.get('l_p') and not kwargs.get('u_p'):
                    if float(product.get('price')) > float(kwargs.get('l_p')):
                        product_list.append(product)
                else:
                    product_list.append(product)
        if kwargs.get('p_s') == 'up' and len(product_list) > 0:
            product_list = sorted(product_list, key=lambda product: product['price'], reverse=False)
        elif kwargs.get('p_s') == 'down' and len(product_list) > 0:
            product_list = sorted(product_list, key=lambda product: product['price'], reverse=True)
        return product_list

    def _check_params(self, **kwargs):
        """参数校验"""
        check_flag = False
        if kwargs.get('webmaster') and (kwargs.get('l_t') in ('w_v', 'l_v')) and kwargs.get('pageIndex') and \
                kwargs.get('pageSize') and (kwargs.get('p_s') in ('default', 'up', 'down',)):
            page_index = int(kwargs.get('pageIndex'))
            page_size = int(kwargs.get('pageSize'))
            if page_index > 0 and page_size > 0:
                check_flag = True
        return check_flag

    def _add_search_times(self, keyword):
        """关键词搜索的次数加一"""
        keyword = keyword.rstrip().lstrip().lower()
        keyword_set = self.get_keyword_set(keyword)
        #按照分词结果查询产品结果集
        for i in xrange(len(keyword_set)):
            keyword_index = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword_set[i]})
            if not keyword_index:
                continue
                #搜索次数加一
            document = {'$inc': {'searchTimes': 1}}
            keyword_index['searchTimes'] += 1
            MongodbUtil.update('shopping', 'keywordIndex', {'_id': keyword_index.get('_id')}, document)

    def _add_glossary(self, keyword):
        """动态填充词汇表"""
        glossary = MongodbUtil.find_one('shopping', 'glossary')
        if not glossary.get('used').__contains__(keyword):
            glossary['used'].append(keyword)
        MongodbUtil.update('shopping', 'glossary', {'_id': glossary.get('_id')}, glossary)

    def get_product_id_list(self, **kwargs):
        """从mongodb中获取产品id结果集"""
        keyword = kwargs.get('keyword').rstrip().lstrip().lower()
        if keyword.__contains__(' '):
            self._add_glossary(keyword)
        keyword_set = self.get_keyword_set(keyword)
        p_id_list_arr = list()
        union_dict = {}
        #按照分词结果查询产品结果集
        for i in xrange(len(keyword_set)):
            keyword_index = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword_set[i]})
            if not keyword_index:
                continue
                #搜索次数加一
            keyword_index['searchTimes'] += 1
            MongodbUtil.update('shopping', 'keywordIndex', {'_id': keyword_index.get('_id')}, keyword_index)
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
            intersection = OrderUtil.order_obj_dict(union_dict, intersection)
        if union_set:
            union_set = OrderUtil.order_obj_dict(union_dict, union_set)

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
        glossary = MongodbUtil.find_one('shopping', 'glossary')
        use_word_list = glossary.get('used')
        un_used_word_list = glossary.get('unUsed')
        for word in use_word_list:
            if keyword.__contains__(word):
                keyword_set.append(word)
        for word in StringUtil.cut_word(keyword):
            if not un_used_word_list.__contains__(word) and not keyword_set.__contains__(word):
                keyword_set.append(word)
        return keyword_set


class HotWordHandler(BaseHandler):
    """
    热词推荐

    """

    def on_request(self):
        try:
            self._event('hot_word')
            keyword = self.params.get('keyword')
            hot_word_response = HotWordResponse(keyword)
            self._jsonify_response(hot_word_response)
        except Exception as e:
            logger.error('[message: %s]' % e.message)


class ImageHandler(BaseHandler):
    """
    图片加载

    """

    def on_request(self):
        try:
            self.load_image(**self.params)
        except Exception as e:
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


class CPCHandler(BaseHandler):
    """
    CPC数据跟踪统计

    """

    def on_request(self):
        try:
            redirect_url, cpc_id = self.cpc_effect(**self.params)
            if not redirect_url:
                self.redirect(url=settings.host_src, permanent=True)
            webmaster = self.params.get('s')
            ad_position_id = self.params.get('a_p_i')
            self.set_cookie('xc_source', webmaster)
            self.set_cookie('c_i', cpc_id.__str__())
            self.set_cookie('a_p_i', ad_position_id)
            self.redirect(url=redirect_url, permanent=True)
        except Exception as e:
            self.cpc_un_effect(cpc_id)
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))

    def cpc_un_effect(self, cpc_id):
        """浏览器异常关闭有效点击数减一"""
        self._event('cpc_un_effect')
        cpc_document = MongodbUtil.find_one('shopping', 'cpc', spec_or_id={'_id': cpc_id})
        if cpc_document:
            cpc_document['takeEffect'] = 0
            result_id = MongodbUtil.update('shopping', 'cpc', spec_or_id={'_id': cpc_id}, document=cpc_document)
            if not result_id:
                self.cpc_un_effect(cpc_id)
            logger.info('Update cpc successful for : %s' % cpc_id)

    def cpc_effect(self, **kwargs):
        """更新点击数及有效点击数"""
        self._event('cpc_effect')
        product_id = kwargs.get('p_i').encode('utf-8')
        exist_product = MongodbUtil.find_one('shopping', 'product', product_id)
        if exist_product:
            cpc_id = self.insert_cpc(exist_product, **kwargs)
            if cpc_id:
                logger.info('Insert cpc successful for : %s' % product_id)
            else:
                logger.warning('Insert cpc error for : %s' % product_id)
            return exist_product.get('url'), cpc_id
        else:
            return None, None

    def insert_cpc(self, product, **kwargs):
        """插入新增点击 takeEffect: 1(successful) 0(failed)"""
        cpc_document = {
            'adPositionId': kwargs.get('a_p_i') if kwargs.get('a_p_i') else '',
            'webmaster': kwargs.get('s'),
            'merchant': product.get('merchantId'),
            'productId': product.get('_id'),
            'clickTime': DateUtil.get_sys_time(),
            'takeEffect': 1,
        }
        obj_id = MongodbUtil.insert('shopping', 'cpc', cpc_document)
        return obj_id


class ManageProductHandler(BaseHandler):
    """
    广告主商品管理

    """

    def on_request(self):
        try:
            #身份验证
            check_auth = CheckUtil.check_auth(**self.params)
            if check_auth:
                method_name = self.params.get('method')
                method_dict = {
                    'search': lambda: self.search_product(**self.params),
                    'modify': lambda: self.modify_product(**self.params),
                    'delete': lambda: self.delete_product(**self.params),
                    'import': lambda: self.import_product(**self.params),
                    'insert': lambda: self.insert_product(**self.params),
                }
                method_dict[method_name]()
            else:
                logger.warning('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                    'Check failed', self.request.host, self.request.remote_ip, self.params.__str__()))
                error_response = BrokenResponse()
                self._jsonify_response(error_response)
        except Exception as e:
            logger.error('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                e.message, self.request.host, self.request.remote_ip, self.params.__str__()))
            error_response = BrokenResponse()
            self._jsonify_response(error_response)

    def insert_product(self, **kwargs):
        """插入部分商品"""
        self._event('insert')
        #解析需要插入的商品信息
        merchant_name = kwargs.get('merchant')
        products = ast.literal_eval(kwargs.get('products'))
        if not (merchant_name and products):
            error_response = BrokenResponse()
            self._jsonify_response(error_response)
            return
            #循环导入每一个商品信息（包含商品图片） 如果导入商品数量过多，则发送异步任务处理
        if len(products) > settings.max_insert_product_size:
            affiliate_celery.send_task('affiliate.task.insert_product.insert_product', args=(products, merchant_name))
        else:
            for product in products:
                do_import_product(product, settings.tag_dict)
                #导入广告主下所有产品的id集合
            import_product_id_2_merchant(merchant_name)
            #返回结果信息
        successful_response = SuccessfulResponse()
        self._jsonify_response(successful_response)

    def import_product(self, **kwargs):
        """导入商品"""
        self._event('import')
        #获取xml文件信息
        file_name = self.request.files['product_file'][0]['filename']
        file_body = self.request.files['product_file'][0]['body']
        if not self.check_file(file_name, file_body):
            logger.warning('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                'Check failed', self.request.host, self.request.remote_ip, self.params.__str__()))
            error_response = BrokenResponse()
            self._jsonify_response(error_response)
            # 将xml文件保存
        file_name = FileUtil.get_filename_by_date('.xml')
        product_list = XMLUtil.read_2_list_by_string(file_body, 'product')
        merchant_name = product_list[0].get('merchant')
        # 插入广告主到数据库
        insert_flag = import_merchant(merchant_name)
        if insert_flag:
            file_path = '%s/productFeeds/%s/' % (settings.files_dir, merchant_name)
            file_path = FileUtil.write_2_file(file_path, file_name, file_body, 'utf-8')
            # 异步导入商品列表
            affiliate_celery.send_task('affiliate.task.import_product.import_product', args=(file_path, merchant_name))
            successful_response = SuccessfulResponse()
            self._jsonify_response(successful_response)
        else:
            broken_response = BrokenResponse()
            self._jsonify_response(broken_response)

    def delete_product(self, **kwargs):
        """删除商品"""
        self._event('delete')
        product_id_list = StringUtil.str_2_list(kwargs.get('productIdList'))
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': kwargs.get('merchant')})
        for product_id in product_id_list:
            product = MongodbUtil.find_one('shopping', 'product', {
                'productId': product_id,
                'merchantId': merchant.get('_id')
            })
            if not product:
                continue
                # 删除广告主中的商品id
            idx = merchant['productIdList'].index(product.get('_id'))
            del merchant['productIdList'][idx]
            MongodbUtil.save('shopping', 'merchant', merchant)
            # 删除倒排索引中的商品id
            keyword_list = product.get('keywordList')
            for keyword in keyword_list:
                existingKeyword = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword})
                if existingKeyword:
                    self.del_keyword_index(keyword, product.get('_id'))
                # 删除商品
            MongodbUtil.delete('shopping', 'product', {
                'productId': product_id,
                'merchantId': merchant.get('_id')
            })
            logger.info('Delete %s\'s product: %s successfully!!!' % (kwargs.get('merchant'), product_id))
        successful_response = SuccessfulResponse()
        self._jsonify_response(successful_response)

    def modify_product(self, **kwargs):
        """商品修改"""
        self._event('modify')
        product = ast.literal_eval(kwargs.get('product'))
        merchant_name = product.get('merchant')
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant_name})
        if not merchant:
            error_response = BrokenResponse()
            self._jsonify_response(error_response)
            return
        exists_product = MongodbUtil.find_one('shopping', 'product', {
            'productId': product.get('productId'),
            'merchantId': merchant.get('_id')
        })
        #获取更新前关键词列表 删除倒排索引中的商品id
        keyword_list_old = exists_product.get('keywordList')
        keyword_list_new = product.get('keywordList')
        for keyword in keyword_list_old:
            if keyword not in keyword_list_new:
                self.del_keyword_index(keyword, exists_product.get('_id'))
            #新增倒排索引中的商品id
        append_keyword_list = list()
        for keyword in keyword_list_new:
            if keyword not in keyword_list_old:
                if keyword:
                    append_keyword_list.append(keyword)
        self.save_keyword_index(append_keyword_list, exists_product.get('_id'))
        #只允许修改keywordList
        for k, v in product.items():
            if k != 'keywordList':
                continue
            exists_product[k] = v
        MongodbUtil.save('shopping', 'product', exists_product)

        successful_response = SuccessfulResponse()
        self._jsonify_response(successful_response)

    def search_product(self, **kwargs):
        """查询产品列表"""
        self._event('search')
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': kwargs.get('merchant')})
        product_id_list = merchant.get('productIdList')
        page_response = ProductPageResponse(product_id_list, **kwargs)
        self._jsonify_response(page_response)

    def del_keyword_index(self, keyword, product_id):
        """删除倒排索引中的商品id"""
        existingKeyword = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword})
        if existingKeyword:
            p_str_id = product_id.__str__()
            if existingKeyword.get('invertedIndex').__contains__(p_str_id):
                del existingKeyword['invertedIndex'][p_str_id]
                status_id = MongodbUtil.save('shopping', 'keywordIndex', existingKeyword)
                if status_id:
                    logger.info('Update keyword: %s successfully!!!' % keyword)
                else:
                    logger.info('Update keyword: %s failed!!!' % keyword)

    def check_file(self, file_name, file_body):
        """检查文件是否符合规范要求"""
        try:
            check_status = False
            if not (file_name.index('.xml') + 4) == len(file_name):
                return check_status
            product_list = XMLUtil.read_2_list_by_string(file_body, 'product')
            product = product_list.pop()
            for k, v in product.items():
                if settings.tag_dict.__contains__(k):
                    continue
                return check_status
            check_status = True
            return check_status
        except Exception:
            return check_status

    def save_keyword_index(self, keyword_set, product_id):
        """遍历keywordList更新倒排索引"""
        for keyword in keyword_set:
            existingKeyword = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword})
            if existingKeyword:
                if not existingKeyword['invertedIndex'].__contains__(product_id.__str__()):
                    existingKeyword['invertedIndex'][product_id.__str__()] = 100.0
                    status_id = MongodbUtil.save('shopping', 'keywordIndex', existingKeyword)
                    if status_id:
                        logger.info('Update keywordIndex: %s successfully!!!' % keyword)
                    else:
                        self.save_keyword_index(keyword_set, product_id)
                        logger.info('Try to update keywordIndex: %s again!!!' % keyword)
            else:
                keywordIndex = {
                    'keyword': keyword,
                    'searchTimes': 0,
                    'invertedIndex': {product_id.__str__(): 100.0},
                }
                status_id = MongodbUtil.insert('shopping', 'keywordIndex', keywordIndex)
                if status_id:
                    logger.info('Save keywordIndex: %s successfully!!!' % keyword)
                else:
                    self.save_keyword_index(keyword_set, product_id)
                    logger.info('Try to update keywordIndex: %s again!!!' % keyword)


class UploadHandler(BaseHandler):
    """
    上传页

    """

    def get(self):
        try:
            self._event('to_upload')
            self.render(settings.upload_template)
        except Exception as e:
            logger.error('[message: %s]' % e.message)
