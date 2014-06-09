#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-17
@description:memcached缓存数据库
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import memcache

from affiliate.config import settings
from affiliate.lib.util.logger_util import logger


class McCache(object):
    """
    缓存工具类
    1.缓存查询数据，避免大量查询阻塞，访问迟缓

    """

    def __init__(self, server=None):
        self._server = server or settings.memcached['default']
        self._mc = memcache.Client(self._server, debug=0)

    def put_obj(self, key, val, timeout):
        """向缓存添加数据"""
        try:
            self._mc.set(key, val, timeout)
        except Exception as e:
            logger.error(e.message)

    def get_obj(self, key):
        """从缓存读取数据"""
        try:
            value = self._mc.get(key)
            return value
        except Exception as e:
            logger.error(e.message)
