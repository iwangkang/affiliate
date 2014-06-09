#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:默认配置信息
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config.base import *

# BASE
DEBUG = False
OFFLINE = False
PRODUCTION = True

#LOG
LOG_PATH = '/home/kratos/log/affiliate'
LOG_FILE = 'affiliate_product.log'
DEFAULT_LOG_SIZE = 1024*1024*50

# MONGONDB
MONGOD_HOST = 'localhost'
MONGOD_PORT = 37017
MONGOD_DBNAME = 'affiliate'

# Merchant list
MERCHANT_LIST = [
    {
        'name': 'FocalPrice'
    }
]

# MEMCACHED
MEMCACHED = {
    'default': ('127.0.0.1:11211', ),
}
SEARCH_TIMEOUT = 60 * 60 * 24

# REBBITMQ

# IMPORT FILES
FILES_DIR = '/home/kratos/files/affiliate'