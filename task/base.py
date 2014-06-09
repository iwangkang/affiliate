#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-17
@description:任务类基类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import logging

from celery import task
from celery.utils.log import get_task_logger

from affiliate.config.celeryconfig import affiliate_celery

logger = get_task_logger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class TaskError(Exception):
    pass


class TaskIOError(TaskError):
    """
    文件操作异常

    """
    pass


class TaskDBError(TaskError):
    """
    数据库操作异常
    """
    pass


@task
def recite():
    """
    测试函数, 随机输出一句诗歌

    """
    poem = '''There's a mirror likeness between those two
shining, youthfully-fledged figures, though
one seems paler than the other and more austere,
I might even say more perfect, more distinguished,
than he, who would take me confidingly in his arms,
how soft then and loving his smile, how blessed his glance!
Then, it might well have been that his wreath
of white poppies gently touched my forehead, at times,
and drove the pain from my mind with its strange scent.
But that is transient. I can only, now, be well,
when the other one, so serious and pale,
the older brother, lowers his dark torch.
Sleep is so good, Death is better, yet
surely never to have been born is best.'''

    fragments = poem.split('\n')

    logger.info('[Heine]: %s' % fragments[random.randint(0, len(fragments) - 1)])

