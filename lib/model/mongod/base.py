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
    client = MongoClient(mongod_host, mongod_port)
    fs = gridfs.GridFS(client[settings.shopping_dbname])


if __name__ == '__main__':
    ps = Base.client[settings.shopping_dbname]['product'].find().skip(0).limit(10).sort([(u'price', 1)])
    ps = list(ps)
    print ps

