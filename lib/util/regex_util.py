#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-2
@description:正则校验工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re


class RegexUtil(object):
    """
    正则校验工具类

    """

    @classmethod
    def email_valid(cls, email):
        """
        邮箱正则验证，
        param email:待验证邮箱字符串
        return True:验证通过
        return False:验证不通过

        """
        try:
            email = str(email)
            email_format = '^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
            if re.match(email_format, email) != None:
                return True
            return False
        except ValueError as e:
            raise e

    @classmethod
    def date_valid(cls, date):
        """
        mysql 日期格式校验
        param date：待验证日期字符串
        return True:验证通过
        return False:验证不通过

        """
        try:
            date = str(date)
            date_format = '^([1-9]{1}[0-9]{3})-(0?[1-9]|1[0-2])-((0?[1-9])|((1|2)[0-9])|30|31)$'
            if re.match(date_format, date):
                return True
            return False
        except ValueError as e:
            raise e