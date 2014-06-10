#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-3-28
@description:网盟后台模块业务逻辑层，处理请求业务逻辑
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import random

from affiliate.config import settings
from tornado.escape import json_encode
from affiliate.views.base import BaseHandler
from affiliate.lib.util.logger_util import logger
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.util.check_util import CheckUtil
from affiliate.lib.util.order_util import OrderUtil
from affiliate.lib.util.math_util import MathUtil
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil
from affiliate.lib.model.db.bson.category import category_name_map
from affiliate.lib.model.models.models import PageResponse, BrokenResponse, ListPageResponse, SuggestResponse


class LoginHandler(BaseHandler):
    """
    登陆

    """
    def get(self):
        try:
            self._event('to_login')
            self.render(settings.login_template)
        except Exception as e:
            logger.error('[message: %s]' % e.message)
            self.render(settings.cms_error_template)

    def post(self):
        try:
            self._event('login_successful')
            username = self.params.get('username')
            password = self.params.get('password')
            if username == 'xingcloud' and password == 'affiliate':
                self.render(settings.cms_index_template)
            else:
                self.render(settings.login_template)
        except Exception as e:
            logger.error('[message: %s]' % e.message)
            self.render(settings.cms_error_template)


class AnalysisHandler(BaseHandler):

    def post(self):
        try:
            self._event('drawing')
            begin_date = DateUtil.str_2_date(self.params.get('begin'), '-')
            end_date = DateUtil.str_2_date(self.params.get('end'), '-')
            print begin_date, end_date
            if not (begin_date and end_date):
                self.write(json_encode({}))
                return
            param = self.get_param(begin_date, end_date)
            self.write(json_encode(param))
        except Exception as e:
            logger.error('[message: %s]' % e.message)

    def get_param(self, begin_date, end_date):
        """获取指定时间范围内的CPC/CPS统计数据 时间由前端来限制：默认都是在一个月内的时间范围，所以天数自动加一即可"""
        days = (end_date - begin_date).days + 1
        cpc_list = MongodbUtil.find('api', 'cpc', spec_or_id={'clickTime': {'$gt': begin_date, '$lt': end_date}}, sort=[(u'clickTime', 1)])
        cps_list = MongodbUtil.find('api', 'cps', spec_or_id={'orderTime': {'$gt': begin_date, '$lt': end_date}}, sort=[(u'orderTime', 1)])
        param = list()
        for i in xrange(days):
            element = list()
            temp_date = '%s-%s-%s' % (begin_date.year, begin_date.month, (begin_date.day + i))
            element.append(temp_date)
            cpc_count = 0
            for cpc in cpc_list:
                click_date = '%s-%s-%s' % (cpc.get('clickTime').year, cpc.get('clickTime').month, cpc.get('clickTime').day)
                if temp_date == click_date and cpc.get('takeEffect') == 1:
                    cpc_count += 1
            element.append(cpc_count)
            cps_count = 0
            for cps in cps_list:
                cps_date = '%s-%s-%s' % (cps.get('orderTime').year, cps.get('orderTime').month, cps.get('orderTime').day)
                if temp_date == cps_date:
                    cps_count += 1
            element.append(cps_count)
            param.append(element)
        return param


# class ListHandler(BaseHandler):
#     """
#     列表页
#
#     """
#
#     def on_request(self):
#         try:
#             #查询数据
#             page_response = self.search_product(**self.params)
#             #以json形式返回数据
#             self._jsonify_response(page_response)
#         except Exception as e:
#             logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))
#             error_response = BrokenResponse()
#             self._jsonify_response(error_response)
#
#     def search_product(self, **kwargs):
#         """
#         查询产品列表
#
#         """
#         #查询参数校验
#         if not self._check_params(**self.params):
#             self._event('check_false')
#             page_response = BrokenResponse()
#             return page_response
#         self._event('%s_list' % kwargs.get('webmaster'))
#         page_response = self._get_product_list(**kwargs)
#         return page_response
#
#     def _check_params(self, **kwargs):
#         """参数校验"""
#         check_flag = False
#         if kwargs.get('webmaster') and kwargs.get('pageIndex') and kwargs.get('pageSize') and (
#                 kwargs.get('p_s') in ('default', 'up', 'down',)) and (
#                 kwargs.get('s_v') in ('default', 'up', 'down')) and category_name_map.__contains__(kwargs.get('c_k')):
#             page_index = int(kwargs.get('pageIndex'))
#             page_size = int(kwargs.get('pageSize'))
#             if page_index > 0 and page_size > 0:
#                 check_flag = True
#         return check_flag
#
#     def _filter_price(self, **kwargs):
#         """获取价格筛选参数"""
#         filter_price = dict()
#         if kwargs.get('l_p') and kwargs.get('u_p'):
#             filter_price['description'] = str(kwargs.get('l_p')) + ' - ' + (kwargs.get('u_p'))
#             filter_price['lower_price'] = kwargs.get('l_p')
#             filter_price['upper_price'] = kwargs.get('u_p')
#         elif not kwargs.get('l_p') and kwargs.get('u_p'):
#             filter_price['description'] = 'Less then ' + (kwargs.get('u_p'))
#             filter_price['lower_price'] = ''
#             filter_price['upper_price'] = kwargs.get('u_p')
#         elif kwargs.get('l_p') and not kwargs.get('u_p'):
#             filter_price['description'] = 'More then ' + str(kwargs.get('l_p'))
#             filter_price['lower_price'] = kwargs.get('l_p')
#             filter_price['upper_price'] = ''
#         else:
#             filter_price = None
#         return filter_price
#
#     def _get_product_list(self, **kwargs):
#         """没有缓存搜索产品列表，搜索并存入缓存"""
#         # TODO 查询出商品的销量添加到商品属性里面，用于界面展示及排序
#         category = category_name_map.get(kwargs.get('c_k'))
#         price_section = self._get_price_section(str(kwargs.get('l_p')), str(kwargs.get('u_p')))
#         merchant_id = None
#         if kwargs.get('m_n'):
#             merchant_id = self._get_merchant_id(kwargs.get('m_n'))
#             if not merchant_id:
#                 page_response = BrokenResponse()
#                 return page_response
#         if category:
#             if kwargs.get('p_s') == 'up':
#                 if price_section:
#                     if merchant_id:
#                         product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category,
#                                                                                'merchantId': merchant_id,
#                                                                                '$where': price_section},
#                                                         sort=[(u'price', 1)])
#                     else:
#                         product_list = MongodbUtil.find('shopping', 'product',
#                                                         spec_or_id={'category': category, '$where': price_section},
#                                                         sort=[(u'price', 1)])
#                 else:
#                     if merchant_id:
#                         product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category,
#                                                                                'merchantId': merchant_id},
#                                                         sort=[(u'price', 1)])
#                     else:
#                         product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category},
#                                                         sort=[(u'price', 1)])
#             elif kwargs.get('p_s') == 'down':
#                 if price_section:
#                     if merchant_id:
#                         product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category,
#                                                                                'merchantId': merchant_id,
#                                                                                '$where': price_section},
#                                                         sort=[(u'price', -1)])
#                     else:
#                         product_list = MongodbUtil.find('shopping', 'product',
#                                                         spec_or_id={'category': category, '$where': price_section},
#                                                         sort=[(u'price', -1)])
#                 else:
#                     if merchant_id:
#                         product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category,
#                                                                                'merchantId': merchant_id},
#                                                         sort=[(u'price', -1)])
#                     else:
#                         product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category},
#                                                         sort=[(u'price', -1)])
#             else:
#                 if price_section:
#                     if merchant_id:
#                         product_list = MongodbUtil.find('shopping', 'product',
#                                                         {'category': category, 'merchantId': merchant_id,
#                                                          '$where': price_section})
#                     else:
#                         product_list = MongodbUtil.find('shopping', 'product', {'category': category, '$where': price_section})
#                 else:
#                     if merchant_id:
#                         product_list = MongodbUtil.find('shopping', 'product',
#                                                         {'category': category, 'merchantId': merchant_id})
#                     else:
#                         product_list = MongodbUtil.find('shopping', 'product', {'category': category})
#             page_response = ListPageResponse(product_list, **kwargs)
#         elif kwargs.get('keyword'):
#             product_id_list = self.get_product_id_list(**kwargs)
#             product_list = self._get_sort_list(merchant_id, product_id_list, **kwargs)
#             page_response = ListPageResponse(product_list, **kwargs)
#         else:
#             page_response = BrokenResponse()
#         return page_response
#
#     def _get_merchant_id(self, merchant_name):
#         """获取商户id"""
#         merchant_id = None
#         if not merchant_name:
#             return merchant_id
#         merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant_name})
#         if merchant:
#             merchant_id = merchant.get('_id')
#
#         return merchant_id
#
#     def _get_price_section(self, lower_price, upper_price):
#         """获得根据价格区间筛选商品"""
#         price_section = None
#         if lower_price and upper_price:
#             price_section = 'this.price > ' + str(lower_price) + ' & this.price < ' + str(upper_price)
#         elif not lower_price and upper_price:
#             price_section = 'this.price < ' + str(upper_price)
#         elif lower_price and not upper_price:
#             price_section = 'this.price > ' + str(lower_price)
#         return price_section
#
#     def _get_sort_list(self, merchant_id, product_id_list, **kwargs):
#         """根据产品id集合过滤排序获取商品列表"""
#         today = DateUtil.get_sys_date()
#         product_list = list()
#         for product_id in product_id_list:
#             product = MongodbUtil.find_one('shopping', 'product', spec_or_id=str(product_id))
#             if merchant_id and product.get('merchantId') != merchant_id:
#                 continue
#             if kwargs.get('f_n') == 'checked':
#                 if product.get('startTime') == today:
#                     if kwargs.get('l_p') and kwargs.get('u_p'):
#                         if (float(product.get('price')) > float(kwargs.get('l_p'))) and \
#                                 (float(product.get('price')) < float(kwargs.get('u_p'))):
#                             product_list.append(product)
#                     elif not kwargs.get('l_p') and kwargs.get('u_p'):
#                         if float(product.get('price')) < float(kwargs.get('u_p')):
#                             product_list.append(product)
#                     elif kwargs.get('l_p') and not kwargs.get('u_p'):
#                         if float(product.get('price')) > float(kwargs.get('l_p')):
#                             product_list.append(product)
#                     else:
#                         product_list.append(product)
#             else:
#                 if kwargs.get('l_p') and kwargs.get('u_p'):
#                     if (float(product.get('price')) > float(kwargs.get('l_p'))) and \
#                             (float(product.get('price')) < float(kwargs.get('u_p'))):
#                         product_list.append(product)
#                 elif not kwargs.get('l_p') and kwargs.get('u_p'):
#                     if float(product.get('price')) < float(kwargs.get('u_p')):
#                         product_list.append(product)
#                 elif kwargs.get('l_p') and not kwargs.get('u_p'):
#                     if float(product.get('price')) > float(kwargs.get('l_p')):
#                         product_list.append(product)
#                 else:
#                     product_list.append(product)
#         if kwargs.get('p_s') == 'up' and len(product_list) > 0:
#             product_list = sorted(product_list, key=lambda product: product['price'], reverse=False)
#         elif kwargs.get('p_s') == 'down' and len(product_list) > 0:
#             product_list = sorted(product_list, key=lambda product: product['price'], reverse=True)
#         return product_list
#
#     def _add_search_times(self, keyword):
#         """关键词搜索的次数加一"""
#         keyword = keyword.rstrip().lstrip().lower()
#         keyword_set = self.get_keyword_set(keyword)
#         #按照分词结果查询产品结果集
#         for i in xrange(len(keyword_set)):
#             keyword_index = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword_set[i]})
#             if not keyword_index:
#                 continue
#                 #搜索次数加一
#             document = {'$inc': {'searchTimes': 1}}
#             keyword_index['searchTimes'] += 1
#             MongodbUtil.update('shopping', 'keywordIndex', {'_id': keyword_index.get('_id')}, document)
#
#     def _add_glossary(self, keyword):
#         """动态填充词汇表"""
#         glossary = MongodbUtil.find_one('shopping', 'glossary')
#         if not glossary.get('used').__contains__(keyword):
#             glossary['used'].append(keyword)
#         MongodbUtil.update('shopping', 'glossary', {'_id': glossary.get('_id')}, glossary)
#
#     def get_product_id_list(self, **kwargs):
#         """从mongodb中获取产品id结果集"""
#         keyword = kwargs.get('keyword').rstrip().lstrip().lower()
#         if keyword.__contains__(' '):
#             self._add_glossary(keyword)
#         keyword_set = self.get_keyword_set(keyword)
#         p_id_list_arr = list()
#         union_dict = {}
#         #按照分词结果查询产品结果集
#         for i in xrange(len(keyword_set)):
#             keyword_index = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword_set[i]})
#             if not keyword_index:
#                 continue
#                 #搜索次数加一
#             keyword_index['searchTimes'] += 1
#             MongodbUtil.update('shopping', 'keywordIndex', {'_id': keyword_index.get('_id')}, keyword_index)
#             p_id_dict = keyword_index.get('invertedIndex')
#             if p_id_dict:
#                 union_dict = dict(union_dict.items() + p_id_dict.items())
#                 p_id_list = sorted(p_id_dict, key=p_id_dict.get, reverse=True)
#                 p_id_list_arr.append(p_id_list)
#                 #结果集排序：先取交集，再取并集(取差集)，分别按照优先级排序，最后合并
#         intersection = list()
#         union_set = list()
#         for i in xrange(len(p_id_list_arr)):
#             if not intersection:
#                 intersection = p_id_list_arr[i]
#                 union_set = p_id_list_arr[i]
#                 continue
#             intersection = list(set(intersection).intersection(set(p_id_list_arr[i])))
#             union_set = list(set(union_set).union(set(p_id_list_arr[i])))
#         if intersection and union_set:
#             union_set = list(set(union_set).difference(set(intersection)))
#             #排序
#         if intersection:
#             intersection = OrderUtil.order_obj_dict(union_dict, intersection)
#         if union_set:
#             union_set = OrderUtil.order_obj_dict(union_dict, union_set)
#
#         product_id_list = list()
#         for i in xrange(len(intersection)):
#             product_id_list.append(intersection[i])
#         for i in xrange(len(union_set)):
#             product_id_list.append(union_set[i])
#         return product_id_list
#
#     def get_keyword_set(self, keyword):
#         """获取关键字无重复集合"""
#         keyword_set = list()
#         #分词模板
#         glossary = MongodbUtil.find_one('shopping', 'glossary')
#         use_word_list = glossary.get('used')
#         un_used_word_list = glossary.get('unUsed')
#         for word in use_word_list:
#             if keyword.__contains__(word):
#                 keyword_set.append(word)
#         for word in StringUtil.cut_word(keyword):
#             if not un_used_word_list.__contains__(word) and not keyword_set.__contains__(word):
#                 keyword_set.append(word)
#         return keyword_set
#
#
# class SuggestHandler(BaseHandler):
#     """
#     推荐逻辑处理
#
#     """
#
#     def get(self):
#         try:
#             page = self.get_suggest_product(**self.params)
#             if len(page.get('suggestItems')) != 0:
#                 self.render(settings.inner_ad_template, page=page)
#             else:
#                 self.render(settings.default_inner_ad_template)
#         except Exception as e:
#             self.render(settings.default_inner_ad_template)
#             logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))
#
#     def get_suggest_product(self, **kwargs):
#         """
#         获取广告位推荐商品集合
#
#         """
#         #查询参数校验
#         page = dict()
#         if not self._check_params(**self.params):
#             self._event('check_false')
#             page['suggestItems'] = list()
#             return page
#         self._event('%s_suggest' % kwargs.get('w_m'))
#         page = self._get_suggest_page(**kwargs)
#         return page
#
#     def _check_params(self, **kwargs):
#         """
#         参数校验
#
#         """
#         check_flag = False
#         # TODO 过滤校验网站主身份
#         if kwargs.get('w_m') and kwargs.get('c_k') and (int(kwargs.get('p_c')) > 0):
#             check_flag = True
#         return check_flag
#
#     def _get_suggest_page(self, **kwargs):
#         """
#         查询数据库获取推荐产品集合
#         1.筛选参数：
#         网站主名称、商品分类、推荐商品个数、价格区间。
#
#         """
#         # 根据筛选参数查库获取推荐商品集合
#         category = category_name_map.get(kwargs.get('c_k'))
#         product_count = kwargs.get('p_c')
#         lower_price = int(kwargs.get('l_p')) if kwargs.get('l_p') else None
#         upper_price = int(kwargs.get('u_p')) if kwargs.get('u_p') else None
#         price_section = None
#         if lower_price or upper_price:
#             price_section = self._get_price_section(lower_price, upper_price)
#
#         product_list = self._get_random_product_list(str(category), price_section, int(product_count))
#
#         # 创建响应对象并返回
#         page_response = SuggestResponse(product_list, **kwargs)
#         return page_response.to_dict()
#
#     def _get_random_product_list(self, category, price_section, product_count):
#         """获取网站主广告位随机推荐商品集合"""
#         if category:
#             if price_section:
#                 product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category, '$where': price_section})
#             else:
#                 product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'category': category})
#         else:
#             if price_section:
#                 product_list = MongodbUtil.find('shopping', 'product', spec_or_id={'$where': price_section})
#             else:
#                 product_list = MongodbUtil.find('shopping', 'product')
#         start_index, end_index = self._get_random_index(len(product_list), product_count)
#         return product_list[start_index: end_index]
#
#     def _get_random_index(self, product_list_length, product_count):
#         """获取随机索引值"""
#         start_index = random.randint(0, product_list_length - product_count)
#         end_index = start_index + product_count
#         return start_index, end_index
#
#     def _get_price_section(self, lower_price, upper_price):
#         """获得根据价格区间筛选商品"""
#         price_section = None
#         if lower_price and upper_price:
#             price_section = 'this.price > ' + str(lower_price) + ' & this.price < ' + str(upper_price)
#         elif not lower_price and upper_price:
#             price_section = 'this.price < ' + str(upper_price)
#         elif lower_price and not upper_price:
#             price_section = 'this.price > ' + str(lower_price)
#         return price_section


# class AnalysisHandler(BaseHandler):
#     """数据统计分析"""
#
#     # Group data by javascript template
#     reduce_cpc_sum_js = """
#     function (obj, cpc) {
#         if(obj.takeEffect == 1){
#             cpc.effectCount++;
#         } else if (obj.takeEffect == 0){
#             cpc.unEffectCount++;
#         }
#     }
#     """
#
#     def on_request(self):
#         try:
#             #身份验证
#             check_auth = CheckUtil.check_auth(**self.params)
#             check_params = self._check_params(**self.params)
#             if not (check_auth and check_params):
#                 error_response = BrokenResponse()
#                 self._jsonify_response(error_response)
#                 return
#             method_name = self.params.get('method')
#             method_dict = {
#                 'cpc': lambda: self.analysis_cpc(**self.params),
#                 'cps': lambda: self.analysis_cps(**self.params),
#             }
#             method_dict[method_name]()
#         except Exception as e:
#             logger.error('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
#                 e.message, self.request.host, self.request.remote_ip, self.params.__str__()))
#             error_response = BrokenResponse()
#             self._jsonify_response(error_response)
#
#     def _check_params(self, **kwargs):
#         """参数校验"""
#         check_flag = False
#         page_index = int(kwargs.get('pageIndex'))
#         page_size = int(kwargs.get('pageSize'))
#         if page_index > 0 and page_size > 0 and kwargs.get('f') and kwargs.get('t'):
#             check_flag = True
#         return check_flag
#
#     def analysis_cps(self, **kwargs):
#         """cps实时统计接口"""
#         self._event('cps_list')
#         page_index = int(kwargs.get('pageIndex'))
#         page_size = int(kwargs.get('pageSize'))
#         product_list, page_count = self._get_cps_item_list(page_index, page_size, **kwargs)
#         page_response = PageResponse(page_index, page_size, page_count, product_list)
#         #返回结果列表信息
#         self._jsonify_response(page_response)
#
#     def _get_cps_item_list(self, page_index, page_size, **kwargs):
#         """查询数据列表"""
#         # 变量声明＆参数赋值
#         item_list, cps_from, cps_to, end_date = list(), kwargs.get('f').lstrip().rstrip(), kwargs.get(
#             't').lstrip().rstrip(), DateUtil.get_sys_date()
#         # 筛选条件
#         spec_or_id, merchant = self._get_condition(cps_from, cps_to)
#         # 查询监控列表
#         cps_list = MongodbUtil.find('shopping', 'cps', spec_or_id=spec_or_id, sort=[(u'cpsTime', 1)])
#         for cps in cps_list:
#             cps['_id'] = cps.get('_id').__str__()
#             cps['webmaster'] = cps_from or cps.get('webmaster')
#             cps['merchant'] = cps_to or merchant.get('name')
#             cps['cpcId'] = cps.get('cpcId').__str__()
#             item_list.append(cps)
#         page_count = MathUtil.round(len(item_list), page_size)
#         item_list = self._filter_cps(item_list, page_index, page_size)
#         return item_list, page_count
#
#     def _filter_cps(self, cps_list, page_index, page_size):
#         """排序过滤监测产品信息"""
#         if page_size > len(cps_list) - (page_index - 1) * page_size:
#             length = len(cps_list) - (page_index - 1) * page_size
#         else:
#             length = page_size
#         return cps_list[(page_index - 1) * page_size: ((page_index - 1) * page_size + length)]
#
#     def analysis_cpc(self, **kwargs):
#         """cpc实时统计接口"""
#         self._event('cpc_list')
#         page_index = int(kwargs.get('pageIndex'))
#         page_size = int(kwargs.get('pageSize'))
#         product_list, page_count = self._get_cpc_item_list(page_index, page_size, **kwargs)
#         page_response = PageResponse(page_index, page_size, page_count, product_list)
#         #返回结果列表信息
#         self._jsonify_response(page_response)
#
#     def _get_cpc_item_list(self, page_index, page_size, **kwargs):
#         """查询数据列表"""
#         # 变量声明＆参数赋值
#         item_list, cpc_from, cpc_to, end_date = list(), kwargs.get('f').lstrip().rstrip(), kwargs.get(
#             't').lstrip().rstrip(), DateUtil.get_sys_date()
#         # 筛选条件
#         condition, merchant = self._get_condition(cpc_from, cpc_to)
#         # 查询监控列表
#         cpc_list = MongodbUtil.group('shopping', collection='cpc', key=['productId', 'webmaster', 'merchant', 'adPositionId', ],
#                                      condition=condition, initial={'effectCount': 0, 'unEffectCount': 0},
#                                      reduce=self.reduce_cpc_sum_js)
#         page_count = MathUtil.round(len(cpc_list), page_size)
#         for cpc in cpc_list:
#             product_id = cpc.get('productId')
#             product = MongodbUtil.find_one('shopping', 'product', {'_id': product_id})
#             start_date = product.get('startTime')
#             product_cpc = {
#                 'title': product.get('title'),
#                 'webmaster': cpc_from,
#                 'merchant': merchant.get('name') or cpc_to,
#                 'startDate': start_date,
#                 'endDate': end_date,
#                 'effectCount': cpc.get('effectCount'),
#                 'unEffectCount': cpc.get('unEffectCount'),
#             }
#             item_list.append(product_cpc)
#         item_list = self._filter_product_cpc(item_list, page_index, page_size)
#         return item_list, page_count
#
#     def _get_condition(self, webmaster_name, merchant_name):
#         """获取筛选条件"""
#         merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant_name})
#         condition = dict()
#         if webmaster_name:
#             condition['webmaster'] = webmaster_name
#         elif merchant:
#             condition['merchant'] = merchant.get('_id')
#         else:
#             condition = None
#         return condition, merchant
#
#     def _filter_product_cpc(self, product_cpc_list, page_index, page_size):
#         """排序过滤监测产品信息"""
#         result_list = list()
#         for i in xrange(len(product_cpc_list)):
#             temp_cpc = None
#             for product_cpc in product_cpc_list:
#                 if not temp_cpc:
#                     temp_cpc = product_cpc
#                     continue
#                 if temp_cpc.get('startTime') > product_cpc.get('startTime'):
#                     temp_cpc = product_cpc
#                     continue
#             result_list.append(temp_cpc)
#             if product_cpc_list:
#                 del product_cpc_list[product_cpc_list.index(temp_cpc)]
#         if page_size > len(result_list) - (page_index - 1) * page_size:
#             length = len(result_list) - (page_index - 1) * page_size
#         else:
#             length = page_size
#         return result_list[(page_index - 1) * page_size: ((page_index - 1) * page_size + length)]