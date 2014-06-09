#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-2
@description:
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class OrderUtil(object):
    """
    排序工具类

    """

    @classmethod
    def order_obj_list(cls, obj_dict, obj_list):
        """
        obj_dict: {'a': 0.99, 'e': 0.79, 'f': 0.89}
        obj_list: ['e', 'f']

        """
        result_list = list()
        order_list = sorted(obj_dict, key=obj_dict.get, reverse=True)
        for i in xrange(len(order_list)):
            if order_list[i] in obj_list:
                result_list.append(order_list[i])
        return result_list


if __name__ == '__main__':
    obj_dict = {'a': 0.99, 'e': 0.79, 'f': 0.89, 'c': 0.76, 'g': 0.98}
    obj_list = ['e', 'f', 'c', 'g']
    result = OrderUtil.order_obj_list(obj_dict, obj_list)
    print result