# #! -*- coding:utf-8 -*-
#
# """
# @author:Conner
# @version:1.0
# @date:13-12-17
# @description:memcached缓存数据库
# """
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# import contextlib
# import Queue
#
# import pylibmc
#
# from affiliate.config import settings
#
#
# class MemcachedCache(object):
#     """
#     缓存数据库
#     根据使用量动态添加链接，解决单进程模式下连接数无意义占用的问题
#
#     """
#     def __init__(self, server=None):
#         self._server = server or settings.memcached['default']
#         self._holder = Queue.Queue(maxsize=settings.memcached_pool_size)
#         self._queue = Queue.Queue()
#
#     @contextlib.contextmanager
#     def reserve(self):
#         try:
#             mc = self._queue.get_nowait()
#         except Queue.Empty:
#             if not self._holder.full():
#                 mc = pylibmc.Client(self._server, binary=True)
#                 try:
#                     self._holder.put_nowait(mc)
#                     self._queue.put_nowait(mc)
#                 except Queue.Full:
#                     pass
#             mc = self._queue.get()
#
#         try:
#             yield mc
#         finally:
#             self._queue.put(mc)
#
#
# memcached = MemcachedCache(settings.memcached['default'])
# warehouse = MemcachedCache(settings.memcached['development'])