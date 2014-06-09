#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-2
@description:更新产品优先级测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.update_priority import update_priority


def test_update_priority():
    update_priority()


if __name__ == '__main__':
    test_update_priority()