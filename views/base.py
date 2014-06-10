#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:处理层基类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import datetime

from tornado import web
from tornado.web import RequestHandler
from tornado.escape import to_unicode

from affiliate.config import settings
from affiliate.lib.util.logger_util import logger


def _flatten_arguments(args):
    """
    去除请求中单值参数的数组结构

    """
    flattened = {}
    for key in args:
        if len(args[key]) == 1:
            flattened[key] = to_unicode(args[key][0])
        else:
            flattened[key] = [to_unicode(arg) for arg in args[key]]

    return flattened


class BaseHandler(RequestHandler):
    """
    逻辑层基类，定义逻辑处理流程

    """
    _cacheable = False
    _label = 'affiliate'

    @web.asynchronous
    def get(self):
        self.on_request()

    @web.asynchronous
    def post(self):
        self.on_request()

    def prepare(self):
        """通过初始化操作"""
        self.params = self._argument()
        self.errors = []
        self.timestamp = time.time()
        self._event('call')
        if settings.offline:
            self.render(settings.offline_template)

    def _argument(self):
        return _flatten_arguments(self.request.arguments)

    def on_request(self):
        raise NotImplementedError

    def on_error(self, error=None):
        self._event('error')

    def on_finish(self):
        self._event('time', int((time.time() - self.timestamp) * 1000))
        self._event('finish')

    def _event(self, event, value=1):
        """通用统计事件输出接口"""
        if not event:
            raise ValueError('event')
        mode = settings.production and 'normal' or 'debug'
        logger.info('%s\t%s\t%s' % (datetime.datetime.utcnow(), '.'.join((mode, self._label, event, )), value,))

    def _jsonify_response(self, response, info=False):
        if not response:
            self.write('Nothing')
            self.finish()
        self.set_header('Cache-Control', 'private')
        self.set_header('Date', datetime.datetime.now())
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        if info:
            logger.info(response.to_json())
        self.write(response.to_json())
        self.finish()