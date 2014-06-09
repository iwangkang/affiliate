#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:错误模块
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.lib.util.logger_util import logger


class Error(Exception):

    def log_message(self):
        logger.error(self.message)


class LoginError(Error):

    def __init__(self, message):
        self.message = message


class RegisterError(Error):

    def __init__(self, message):
        self.message = message


class MerchantError(Error):

    def __init__(self, message):
        self.message = message


class WebmasterError(Error):

    def __init__(self, message):
        self.message = message


class UploadError(Error):

    def __init__(self, message):
        self.message = message