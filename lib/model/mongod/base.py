#coding=utf8
__author__ = 'changdongsheng'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import gridfs

from pymongo import MongoClient
from affiliate.config import settings


class Base(object):
    """
    mongodb基类

    """

    mongod_host = settings.mongod_host
    mongod_port = settings.mongod_port
    mongod_dbname = settings.mongod_dbname

    client = MongoClient(mongod_host, mongod_port)
    db = client[mongod_dbname]

    fs = gridfs.GridFS(db)

