#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-9
@description:文件工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import time
import codecs


class FileUtil(object):
    """
    文件工具类

    """

    @classmethod
    def read_file_content(cls, file_path, encoding):
        try:
            file = codecs.open(file_path, 'r', encoding)
            content = file.read()
            return content
        finally:
            file.close()

    @classmethod
    def read_file_line_content(cls, file_path, encoding):
        try:
            file = codecs.open(file_path, 'r', encoding)
            line = file.readline()
            return line
        finally:
            file.close()

    @classmethod
    def read_file_lines_content(cls, file_path, encoding):
        try:
            file = codecs.open(file_path, 'r', encoding)
            lines = file.readlines()
            return lines
        finally:
            file.close()

    @classmethod
    def write_2_file(cls, file_path, file_name, content, encoding):
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path = file_path + file_name
            file = codecs.open(file_path, 'a', encoding)
            file.write(str(content).decode(encoding))
            return file_path
        finally:
            file.close()

    @classmethod
    def get_filename_by_date(cls, suffix):
        local_time = time.localtime()
        if suffix.__contains__('.'):
            file_name = '%s_%s_%s_%s_%s_%s%s' % (local_time.tm_year, local_time.tm_mon, local_time.tm_yday,
                                                 local_time.tm_hour, local_time.tm_min, local_time.tm_sec, suffix)
        else:
            file_name = '%s_%s_%s_%s_%s_%s.%s' % (local_time.tm_year, local_time.tm_mon, local_time.tm_yday,
                                                  local_time.tm_hour, local_time.tm_min, local_time.tm_sec, suffix)
        return file_name

if __name__ == '__main__':
    print FileUtil.get_filename_by_date('xml')