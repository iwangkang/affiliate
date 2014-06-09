#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-23
@description:线程池
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import random

from threading import RLock
from affiliate.lib.model.pool.easypool.easypool import ThreadPool


from affiliate.config import settings


class MyThreadPool(object):
    """
    自定义线程池

    """

    thread_lock = RLock()

    def __init__(self, num_threads, min_pool=0, max_pool=0, send_item=False, queue_type='fifo'):
        self.__thread_lock = RLock()
        self.__init_thread_pool(num_threads, send_item, min_pool, max_pool, queue_type)

    def __init_thread_pool(self, num_threads, send_item=False, min_pool=0, max_pool=0, queue_type='fifo'):
        """获取线程池实例对象"""
        if not min_pool:
            min_pool = settings.default_min_pool
        if not max_pool:
            max_pool = settings.default_max_pool

        self.__pool = ThreadPool(num_threads, send_item, min_pool, max_pool, queue_type)

    def wait_completion(self):
        """等待队列中的所有任务的完成"""
        self.__pool.wait_completion()

    def add_task(self, func, *args, **kwargs):
        """添加任务到线程池"""
        self.__pool.add_task(func, *args, **kwargs)
