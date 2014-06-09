#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-5
@description:日期库
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

from datetime import datetime, timedelta


class DateUtil(object):
    """
    提供系统所需日期时间等相关静态数据

    """

    @classmethod
    def get_end_date(cls, start_date, alive_days):
        """获取过期日期"""
        start_date_arr = str(start_date).split('-')
        start_date = datetime(int(start_date_arr[0]), int(start_date_arr[1]), int(start_date_arr[2]))
        alive_days = timedelta(days=alive_days)
        end_date = start_date + alive_days
        return end_date.strftime('%Y-%m-%d')

    @classmethod
    def get_sys_date(cls):
        """系统当前日期"""
        local_time = time.localtime()
        sys_date = time.strftime('%Y-%m-%d', local_time)
        return sys_date

    @classmethod
    def get_sys_time(cls):
        """系统当前时间"""
        local_time = time.localtime()
        sys_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        return sys_time


if __name__ == '__main__':
    print DateUtil.get_sys_date()
    # start_date = '2014-01-06'
    # alive_days = 30
    # end_date = DateUtil.get_end_date(start_date, alive_days)
    # print end_date
    # print start_date > end_date