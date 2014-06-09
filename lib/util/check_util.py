#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-14
@description:校验工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import ast


class CheckUtil(object):
    """
    校验工具类

    """

    @classmethod
    def check_auth(cls, **kwargs):
        """接口调用身份验证"""
        check_status = False
        params = ast.literal_eval(kwargs.get('p'))
        result = float(kwargs.get('r'))
        if not params:
            return check_status
        square = 1
        compute_result = 0
        for param in params:
            compute_result += param + 2**square
            square += 1
        compute_result = float(str(float(compute_result) / float(len(params)))[:10])
        if compute_result == result:
            check_status = True
        return check_status


if __name__ == '__main__':
    p = {
        'params': u'[1, 2, 3, 783, 123, 0]',
        'result': u'173.0',
    }
    check_result = CheckUtil.check_auth(**p)
    print check_result



