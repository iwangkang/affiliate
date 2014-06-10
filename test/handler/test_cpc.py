#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-2
@description:cpc测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import urllib2

from affiliate.lib.model.pool.thread_pool import MyThreadPool


urls = [
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a3046d',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a3046e',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a3046a',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a3046b',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a3046c',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1baa9ce7c76363a2ea9a',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1baa9ce7c76363a2ea9b',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30465',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30466',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30467',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30460',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30461',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30462',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30463',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bfb9ce7c76363a30468',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bd29ce7c76363a2f833',
    'http://affiliate.xingcloud.com/cpc?source=123456&productId=52fb1bd29ce7c76363a2f832',
]


def test_single_request():
    """单个搜索请求"""
    index = random.randint(0, urls.__len__()-1)
    url = urls[index]
    print(url)
    result = urllib2.urlopen(url)
    print result


def test_concurrent_request():
    """压力测试"""
    product_pool = MyThreadPool(num_threads=167, min_pool=69, max_pool=512)
    for i in xrange(10000):
        product_pool.add_task(test_single_request)
    product_pool.wait_completion()


if __name__ == '__main__':
    import time
    while True:
        test_single_request()
        time.sleep(2)
    # test_concurrent_request()