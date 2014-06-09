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
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5c4ccf4f0f2b0437dc',
    'http://affiliate.xingcloud.com/image?filename=517a306b158b4f7b911448b467f3232b_128x128.png',
    'http://affiliate.xingcloud.com/image?filename=6cdb794d498f44fa99bebc26a0e54e17_128x128.png',
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5c4ccf4f0f2b0437ac',
    'http://affiliate.xingcloud.com/image?filename=5121095ad8fa4c1783ab65fcd9f621b6_128x128.png',
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5c4ccf4f0f2b04386f',
    'http://affiliate.xingcloud.com/image?filename=0406c13e20914117879cdfbc95bd6b92_128x128.png',
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5c4ccf4f0f2b0437f2',
    'http://affiliate.xingcloud.com/image?filename=86af28de4f01412db988f4a89233e850_128x128.png',
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5c4ccf4f0f2b0437e6',
    'http://affiliate.xingcloud.com/image?filename=5d1ffcfd8fe249c1a3740ef27c5c7431_128x128.png',
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5e4ccf4f0f2b0438f8',
    'http://affiliate.xingcloud.com/image?filename=6d197af80f284bdcbbd8f917b31d4006_210x210.png',
    'http://affiliate.xingcloud.com/product?source=123456&productId=52c65e5c4ccf4f0f2b0438ba',
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
    # test_single_request()
    test_concurrent_request()