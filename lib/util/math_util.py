#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-20
@description:数学计算工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MathUtil(object):
    """
    数学计算工具类

    """

    @classmethod
    def round(cls, dividend, divisor):
        """四入五入"""
        mod = int(dividend) % int(divisor)
        if not mod:
            return int(dividend) / int(divisor)
        else:
            return (int(dividend) / int(divisor)) + 1

    @classmethod
    def parse2percent(cls, str_or_float):
        """百分化"""
        if not str_or_float:
            return None
        if isinstance(str_or_float, float):
            str_or_float = str(str_or_float)
        str_arr = str_or_float.split('.')
        if str_arr[0] == '0':
            return float(str_or_float)
        divisor = float(10 ** len(str_arr[0]))
        percentage = float(str_or_float) / divisor
        return percentage


if __name__ == '__main__':
    result = MathUtil.parse2percent(12365.56)
    print result