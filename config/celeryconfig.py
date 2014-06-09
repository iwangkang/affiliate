#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-9
@description:celery配置文件
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from celery import Celery
from datetime import timedelta
from kombu import Queue, Exchange
from affiliate.config import settings


class BaseConfig(object):
    CELERY_ACKS_LATE = True

    CELERY_QUEUES = (
        Queue('proxy_import_product', Exchange('proxy_import_product'), routing_key='proxy.import.product'),
        Queue('clear_update_product', Exchange('clear_update_product'), routing_key='clear.update.product'),
    )

    CELERY_ROUTES = {
        'affiliate.task.import_product.import_product': {
            'queue': 'proxy_import_product',
            'routing_key': 'proxy.import.product',
        },
        'affiliate.task.timed_task.clear_update_product': {
            'queue': 'clear_update_product',
            'routing_key': 'clear.update.product',
        },
    }

    CELERY_IMPORTS = (
        'affiliate.task.import_product',
        'affiliate.task.timed_task',
    )

    CELERYBEAT_SCHEDULE = {
        'clear_update_product_every_day': {
            'task': 'affiliate.task.timed_task.clear_update_product',
            'schedule': timedelta(days=1),
            'args': ()
        },
    }

    # Email相关设置
    CELERY_SEND_TASK_ERROR_EMAILS = True
    ADMINS = (
        ('wangkang', 'wangkang@xingcloud.com'),
    )
    SERVER_EMAIL = 'Distributed Translation<xcmonitor01@163.com>'
    EMAIL_HOST = 'smtp.163.com'
    EMAIL_HOST_USER = 'xcmonitor01@163.com'
    EMAIL_HOST_PASSWORD = 'xingcloud'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    EMAIL_TIMEOUT = 10


class DevelopmentConfig(BaseConfig):
    BROKER_URL = settings.rabbitmq_broker_url


class ProductionConfig(BaseConfig):
    BROKER_URL = settings.rabbitmq_broker_url


affiliate_celery = Celery()

AFFILIATE_ENV = os.environ.get('AFFILIATE_ENV', 'development')

print 'AFFILIATE_ENV: %s' % AFFILIATE_ENV

if AFFILIATE_ENV in ['production']:
    affiliate_celery.config_from_object(ProductionConfig)
elif AFFILIATE_ENV in ['development']:
    affiliate_celery.config_from_object(DevelopmentConfig)
else:
    raise Exception('AFFILIATE Error, Celery configure file import error.')