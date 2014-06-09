#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-5
@description:日期测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.lib.util.date_util import DateUtil


if __name__ == '__main__':
    print(DateUtil.get_sys_date())