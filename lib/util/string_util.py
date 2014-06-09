#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:字符串工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import hashlib
from datetime import datetime

from affiliate.config import settings


class StringUtil(object):
    """
    字符串工具类

    """

    @classmethod
    def str_2_list(cls, str):
        """
        字符串转成列表

        """
        str = str.replace('[', '').replace(']', '').replace('\'', '').replace('\"', '').encode('utf-8')
        str_list = str.split(',')
        return str_list

    @classmethod
    def replace_by_dict(cls, former_str, replace_dict):
        """
        成组替换字符串

        """
        for k, v in replace_dict.items():
            former_str = former_str.replace(k, v)
        return former_str

    @classmethod
    def str2md5(cls, string):
        """
        获得字符串md5加密后的值

        """
        m = hashlib.md5()
        m.update(str(string))
        return m.hexdigest()

    @classmethod
    def date_parser(cls, date_str):
        """
        解析多种格式的日期字符串数据

        :param date_str: 日期字符串
        :type date_str: str
        """
        supported = [
            '%m/%d/%Y',
            '%m-%d-%Y',
            '%Y-%m-%d',
            '%m/%d/%Y %H:%M',
            '%m-%d-%Y %H:%M',
        ]

        date = None
        date_str = date_str.strip()

        for fm in supported:
            try:
                date = datetime.strptime(date_str, fm)

                if date:
                    break
            except ValueError:
                continue
        if not date:
            raise ValueError
        return date

    @classmethod
    def check_contains_separator(cls, word):
        for separator in settings.word_separator:
            if word.__contains__(separator):
                return True, separator
        return False, None

    @classmethod
    def clean_list(cls, wait_4_clean_list):
        """替换清洗"""
        clean_word_list = list()
        for i in xrange(len(wait_4_clean_list)):
            clean_word = wait_4_clean_list[i].lstrip().rstrip()
            if clean_word:
                for k, v in settings.word_replace.items():
                    if clean_word.__contains__(k):
                        clean_word = clean_word.lower().replace(k, v)
                if clean_word:
                    clean_word_list.append(clean_word)

        return clean_word_list

    @classmethod
    def cut_word(cls, word):
        """
        切词函数
        field@word:待切割语句

        """
        cut_result_list = list()
        wait_4_cut_list = list()
        wait_4_cut_list.append(word)
        while wait_4_cut_list:
            word = wait_4_cut_list.pop()
            if word:
                word = word.lstrip().rstrip().lower()
                cut_flag, separator = cls.check_contains_separator(word)
                if not cut_flag:
                    if not cut_result_list.__contains__(word):
                        cut_result_list.append(word)
                    continue
                cut_list = word.split(separator)
                for w in cut_list:
                    cut_flag, separator = cls.check_contains_separator(w)
                    if cut_flag:
                        wait_4_cut_list.append(w)
                    else:
                        if not cut_result_list.__contains__(w):
                            cut_result_list.append(w)
        clean_result = cls.clean_list(cut_result_list)
        # clean_result = [item.strip("\"\',;.{}()\n") for item in cut_result_list]
        return clean_result


if __name__ == '__main__':
    str = "['CA392L', 'CA396L', 'CA404L']"
    result = StringUtil.str_2_list(str)
    print type(result)