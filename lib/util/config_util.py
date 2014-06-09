#coding=utf8
__author__ = 'changdongsheng'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def setting_from_object(obj):
    u"""转化配置文件为dict 对象，配置文件中得所有大写的配置项目都回转换成全小写的key
    """
    settings = dict()
    for key in dir(obj):
        if key.isupper():
            settings[key.lower()] = getattr(obj, key)
    return settings