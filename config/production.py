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

#SRC
HOST_SRC = 'http://affiliate.xingcloud.com'

#LOG
LOG_PATH = '/home/kratos/log/affiliate'
LOG_FILE = 'affiliate_product.log'
DEFAULT_LOG_SIZE = 1024*1024*50

# MONGONDB
MONGOD_HOST = 'localhost'
MONGOD_PORT = 37017
SHOPPING_DBNAME = 'shopping'
API_DBNAME = 'api'

# MEMCACHED
MEMCACHED = {
    'default': ('127.0.0.1:11211', ),
}
INDEX_TIMEOUT = 60 * 9
SEARCH_TIMEOUT = 60 * 60 * 24
SEARCH_NEW_HOT_TIMEOUT = 60 * 3

# REBBITMQ
RABBITMQ_BROKER_URL = "amqp://kratos_v2:GZLxVSdOQTIIKGpeoC3vv5Myh@50.23.186.242:5672/affiliate"

# IMPORT FILES
FILES_DIR = '/home/kratos/files/affiliate'
