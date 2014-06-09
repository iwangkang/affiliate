#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-18
@description:导入配置信息到setting对象
"""
import os
from . import development, production
from affiliate.lib.util.config_util import setting_from_object
from affiliate.lib.util.dict2object import Dict2Obj

#加载环境变量
AFFILIATE_ENV = os.environ.get('AFFILIATE_ENV', 'development')

config = development

if AFFILIATE_ENV.lower() in ["production"]:
    config = production

settings = Dict2Obj(setting_from_object(config))

del AFFILIATE_ENV