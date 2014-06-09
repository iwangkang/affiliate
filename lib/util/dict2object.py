#coding=utf8
__author__ = 'changdongsheng'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Dict2Obj(object):
    def __init__(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                setattr(self, k, v)

    def configure(self, key, value):
        setattr(self, key.lower(), value)