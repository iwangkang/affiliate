#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-3
@description:图片处理测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.lib.util.image_util import ImageCover


def test_advertiser_logo():
    params = {
        'filename': 'D:\\test.png',
    }

    im = ImageCover(**params)
    im.advertiser_logo()


