#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-1-6
@description:测试导出关键词
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.export_keyword import export_keyword


def test_export_keyword(file_path, file_name):
    export_keyword(file_path, file_name)


if __name__ == '__main__':
    file_path = 'D:/'
    file_name = 'keyword.txt'
    test_export_keyword(file_path, file_name)