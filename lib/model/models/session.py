#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-6-3
@description:会话模块
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


import hashlib
from affiliate.lib.util.date_util import DateUtil


class Session(object):
    """
    会话

    """

    @classmethod
    def get_session_id(cls):
        current_time = DateUtil.get_sys_time(format_str='%Y-%m-%d %H:%M:%S')
        session_id = hashlib.md5(current_time).hexdigest()
        return session_id


if __name__ == '__main__':
    session_id = Session.get_session_id()
    print session_id