#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-29
@description:图片上传工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import uuid
import traceback

from PIL import Image
from cStringIO import StringIO

from affiliate.lib.util.image_util import ImageCover
from affiliate.lib.model.error.error import UploadError
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


class UploadUtil(object):
    """
    图片上传工具类

    """

    @classmethod
    def upload_pic(cls, file_name, file_body, width=128, height=128):
        """上传logo到mangodb"""
        try:
            file_name = cls.get_unique_name(file_name, width, height)
            content = StringIO(file_body)
            img = Image.open(content)
            cover = ImageCover(img)
            format_size = (int(width), int(height))
            # img = cover.thumbnail(format_size)
            img = cover.resize(format_size)
            filename = MongodbUtil.put(file_name, img)
            return filename
        except UploadError as e:
            e.log_message(traceback.print_exc())

    @classmethod
    def get_unique_name(cls, file_name, width=128, height=128, length=32):
        """生成唯一文件名"""
        file_name = file_name[str(file_name).rfind('/')+1:len(file_name)]
        file_name_arr = file_name.split('.')
        suffix = file_name_arr[1]
        unique_id = uuid.uuid4().hex[:length]
        unique_name = '%s_%sx%s' % (str(unique_id), str(width), str(height))
        return unique_name


if __name__ == '__main__':
    filename = 'http://img.focalprice.com/860x666/IM/IM0106/IM0106T-1.JPG'
    unique_name = UploadUtil.get_unique_name(filename)
    print(unique_name)