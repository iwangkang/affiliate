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
DEBUG = True
OFFLINE = False
PRODUCTION = False

#SRC
HOST_SRC = 'http://localhost:9898'

#LOG
LOG_PATH = '/home/kratos/log/affiliate'
LOG_FILE = 'affiliate_development.log'
DEFAULT_LOG_SIZE = 1024*1024*50

# MONGONDB
MONGOD_HOST = 'localhost'
MONGOD_PORT = 27017
SHOPPING_DBNAME = 'shopping'
API_DBNAME = 'api'

# MEMCACHED
MEMCACHED = {
    'default': ('127.0.0.1:11211', ),
}
INDEX_TIMEOUT = 60 * 60 * 24
SEARCH_TIMEOUT = 60 * 60 * 24
SEARCH_NEW_HOT_TIMEOUT = 60 * 3

# REBBITMQ
RABBITMQ_BROKER_URL = "amqp://kratos:GZLxVSdOQTIIKGpeoC3vv5Myh@10.1.15.194:5672/affiliate"

# IMPORT FILES
FILES_DIR = 'D:/files'