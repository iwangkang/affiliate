#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-2
@description:正则测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.lib.util.regex_util import RegexUtil


if __name__ == '__main__':
    email = 'wangkang321_123@xingcloud.com'
    date = '2013-12-01'
    flag = RegexUtil.email_valid(email)
    print(flag)
    flag = RegexUtil.date_valid(date)
    print(flag)