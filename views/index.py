#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-8-19
@description:业务逻辑层，处理请求业务逻辑
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.config import settings
from affiliate.views.base import BaseHandler


class IndexHandler(BaseHandler):
    """
    首页

    """
    def get(self):
        self.render(settings.index_template)


class UploadHandler(BaseHandler):
    """
    上传

    """
    def get(self):
        self.render(settings.upload_template)