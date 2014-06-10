#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-4-1
@description:用户行为跟踪统计逻辑
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import ujson as json

from tornado.web import utf8
from tornado.escape import json_encode
from bson.objectid import ObjectId
from affiliate.config import settings
from affiliate.views.base import BaseHandler
from affiliate.lib.util.logger_util import logger
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.model.models.session import Session
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


class CPCHandler(BaseHandler):
    """
    CPC数据跟踪统计

    """

    def get(self):
        try:
            user_id = self.get_cookie('u_i') if self.get_cookie('u_i') else Session.get_session_id()
            redirect_url, cpc_id = self.cpc_effect(user_id, **self.params)
            if not redirect_url:
                self.redirect(url=settings.host_src, permanent=True)
            self.set_cookie('u_i', user_id, expires_days=settings.cookie_alive_time)
            self.set_cookie('xc_source', 'xingcloud', expires_days=settings.cookie_alive_time)
            self.set_cookie('m_c', self.params.get('m_c'), expires_days=settings.cookie_alive_time)
            self.set_cookie('c_i', cpc_id.__str__(), expires_days=settings.cookie_alive_time)

            self.redirect(url=redirect_url, permanent=True)
        except Exception as e:
            self.cpc_un_effect(cpc_id)
            logger.error('[message: %s]; [params: %s]' % (e.message, self.params.__str__()))

    def cpc_un_effect(self, cpc_id):
        """浏览器异常关闭有效点击数减一"""
        self._event('cpc_un_effect')
        cpc_document = MongodbUtil.find_one('api', 'cpc', spec_or_id={'_id': cpc_id})
        if cpc_document:
            cpc_document['takeEffect'] = 0
            result_id = MongodbUtil.update('api', 'cpc', spec_or_id={'_id': cpc_id}, document=cpc_document)
            if not result_id:
                self.cpc_un_effect(cpc_id)
            logger.info('Update cpc successful for : %s' % cpc_id)

    def cpc_effect(self, user_id, **kwargs):
        """更新点击数及有效点击数"""
        self._event('cpc_effect')
        language, title, webmaster, merchant, category, url, meta_info, duration = kwargs.get('l_g'), kwargs.get(
            't_t_l') if kwargs.get('a_p_i') else '', kwargs.get('w_m'), kwargs.get('m_c'), kwargs.get(
            'c_g'), kwargs.get('url'), kwargs.get('m_i'), kwargs.get('d_t')
        if webmaster and merchant and language and url and category:
            cpc_id = self.insert_cpc(user_id, language, title, webmaster, merchant, category, url, meta_info, duration)
            if cpc_id:
                logger.info('Insert cpc successful for : %s' % url)
                return url, cpc_id
            else:
                logger.warning('Insert cpc error for : %s' % url)
        return None, None

    def insert_cpc(self, user_id, language, title, webmaster, merchant, category, url, meta_info, duration):
        """插入新增点击 takeEffect: 1(successful) 0(failed)"""
        cpc_document = {
            'uid': user_id,
            'merchant': merchant,
            'clickTime': DateUtil.get_sys_time(),
            'url': url,
            'takeEffect': 	1,
            'webmaster': webmaster,
            'category': category,
            'language': language,
            'title': title,
            'metaInfo': meta_info,
            'duration': duration,
        }
        obj_id = MongodbUtil.insert('api', 'cpc', cpc_document)
        return obj_id


class CPSHandler(BaseHandler):
    """
    跨域处理逻辑

    """
    CALLBACK = 'callback'       # define callback argument name

    def get(self):
        try:
            method_name = self.params.get('callback')
            method_dict = {
                'order': lambda: self._set_cps(**self.params),
                'suc': lambda: self._update_cps_status(),
            }
            method_dict[method_name]()
        except Exception as e:
            logger.error('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                e.message, self.request.host, self.request.remote_ip, self.params.__str__()))

    def post(self):
        try:
            method_name = self.params.get('callback')
            method_dict = {
                'order': lambda: self._set_cpsuc(**self.params),
            }
            method_dict[method_name]()
        except Exception as e:
            logger.error('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                e.message, self.request.host, self.request.remote_ip, self.params.__str__()))

    def _update_cps_status(self):
        """更新订单状态为成功"""
        self._event('update_status')
        cps_id_str = self.get_cookie('c_i_l')
        cps_id_list = cps_id_str.split('_') if cps_id_str else list()
        for cps_id in cps_id_list:
            if cps_id:
                cps_document = MongodbUtil.find_one('api', 'cps', spec_or_id={'_id': ObjectId(cps_id)})
                if cps_document:
                    cps_document['status'] = 'successful'
                    cps_document['successfulTime'] = DateUtil.get_sys_time()
                    MongodbUtil.update('api', 'cps', spec_or_id={'_id': cps_document.get('_id')}, document=cps_document)
        self.set_cookie('c_i_l', '', expires_days=settings.cookie_alive_time)
        result_info = {
            'status': '200',
            'message': 'successful',
        }
        self.write(json_encode(result_info))

    def _set_cpsuc(self, **kwargs):
        try:
            self._event('cpsuc')
            order_list = json.loads(kwargs.get('orderList'))
            self._cpsuc_effect(order_list)
            result_info = {
                'status': '200',
                'message': 'successful',
            }
            self.write(json_encode(result_info))
        except Exception as e:
            logger.error('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                e.message, self.request.host, self.request.remote_ip, self.params.__str__()))

    def _cpsuc_effect(self, order_list):
        for order in order_list:
            # 获取校验参数
            if type(order) is dict and order.has_key('merchant') and order.has_key('orderId') and order.has_key('productList') and order.has_key('merchant'):
                exist_order = MongodbUtil.find_one('api', 'cps', spec_or_id={'orderId': order.get('orderId'), 'merchant': order.get('merchant')})
                if exist_order:
                    exist_order['status'] = 'successful'
                    exist_order['successfulTime'] = DateUtil.get_sys_time()
                    MongodbUtil.update('api', 'cps', spec_or_id={'_id': exist_order.get('_id')}, document=exist_order)
                    continue
            else:
                continue
            order = self._fit_params(order)
            # 插入cps
            cps_id = MongodbUtil.insert('api', 'cps', order)
            if cps_id:
                self._event('cps_insert:%s' % cps_id)

    def _set_cps(self, **kwargs):
        try:
            self._event('cps')
            order_list = json.loads(kwargs.get('orderList'))
            merchant = self.get_cookie('m_c')
            self._cps_effect(merchant, order_list)
            result_info = {
                'status': '200',
                'message': 'successful',
            }
            self.write(json_encode(result_info))
        except Exception as e:
            logger.error('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                e.message, self.request.host, self.request.remote_ip, self.params.__str__()))

    def _cps_effect(self, merchant, order_list):
        """广告主订单成功，在联盟插入cps数据，确认cps生效"""
        cookie_value = ''
        for order in order_list:
            # 获取校验参数
            if type(order) is dict and order.has_key('merchant') and order.has_key('orderId') and order.has_key('productList') and order.has_key('merchant') and (merchant == order.get('merchant')):
                exist_order = MongodbUtil.find_one('api', 'cps', spec_or_id={'orderId': order.get('orderId'), 'merchant': order.get('merchant')})
                if exist_order:
                    exist_order['status'] = 'successful'
                    exist_order['successfulTime'] = DateUtil.get_sys_time()
                    MongodbUtil.update('api', 'cps', spec_or_id={'_id': exist_order.get('_id')}, document=exist_order)
                    continue
            else:
                continue
            order = self._fit_params(order)
            # 插入cps
            cps_id = MongodbUtil.insert('api', 'cps', order)
            if cps_id:
                self._event('cps_insert:%s' % cps_id)
                cookie_value += '_%s' % cps_id.__str__()
        if cookie_value:
            self.set_cookie('c_i_l', cookie_value, expires_days=settings.cookie_alive_time)

    def _fit_params(self, order):
        """获取符合格式的参数"""
        cpc_id = self.get_cookie('c_i') if self.get_cookie('c_i') else ''
        order['orderTime'] = DateUtil.get_sys_time()
        order['status'] = 'pendding'
        order_total_price = order.get('orderTotalPrice') if order.get('orderTotalPrice') else 0.0
        if not order_total_price:
            for product in order.get('productList'):
                order_total_price += product.get('totalPrice')
            order['orderTotalPrice'] = order_total_price
        if cpc_id:
            order['cpcId'] = ObjectId(cpc_id)

        return order

    def finish(self, chunk=None):
        """Finishes this response, ending the HTTP request."""
        assert not self._finished
        if chunk:
            self.write(chunk)

        # get client callback method
        callback = utf8(self.get_argument(self.CALLBACK))
        # format output with jsonp
        self._write_buffer.insert(0, callback + '(')
        self._write_buffer.append(')')

        # call base class finish method
        super(CPSHandler, self).finish() # chunk must be None