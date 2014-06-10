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

import os
import random
import logging

from celery import task
from celery.utils.log import get_task_logger

from affiliate.config import settings
from affiliate.config.celeryconfig import affiliate_celery
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def _get_logger():
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(settings.log_path, settings.log_file),
        maxBytes=settings.default_log_size,
        backupCount=9,
        encoding="utf-8",
    )
    logger = get_task_logger(__name__)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    return logger


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


def get_merchant_list():
    """
    获取广告主列表

    """
    merchant_name_list = list()
    merchant_list = MongodbUtil.find('shopping', 'merchant')
    for merchant in merchant_list:
        merchant_name_list.append(merchant.get('name'))
    return merchant_name_list


logger = _get_logger()


if __name__ == '__main__':
    logger.info('sdfsfsf')