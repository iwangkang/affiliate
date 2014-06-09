#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-3
@description:缓存测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

from affiliate.lib.model.cache.memcache_win import McCache


def test_memcached():
    mc = McCache()
    mc.put_obj('some_key', 'some_value', 5)
    time.sleep(3)
    value = mc.get_obj('some_key')
    print value


if __name__ == '__main__':
    test_memcached()
    mc = McCache()
    time.sleep(3)
    value = mc.get_obj('some_key')
    print value