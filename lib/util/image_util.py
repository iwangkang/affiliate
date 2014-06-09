#coding=utf8
__author__ = 'changdongsheng'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from PIL import Image


class ImageCover(object):
    def __init__(self, image):
        if image:
            self.__im = image

    def thumbnail(self, format_size):
        raw_size = self.__im.size
        if raw_size[0] < format_size[0] or raw_size[1] < format_size[1]:
            return self.__im
        x_scale = raw_size[0]/format_size[0]
        y_scale = raw_size[1]/format_size[1]
        min_scale = min(x_scale, y_scale)
        s_x = (raw_size[0] - min_scale * format_size[0])/2
        s_y = (raw_size[1] - min_scale * format_size[1])/2
        box = (s_x, s_y, format_size[0]*min_scale+s_x, format_size[1]*min_scale+s_y)
        region_im = self.__im.crop(box)
        region_im.thumbnail(format_size, Image.ANTIALIAS)
        return region_im

    def resize(self, format_size):
        img = self.__im.resize(format_size, Image.ANTIALIAS)
        return img


if __name__ == "__main__":
    im = Image.open('d:/test.png')
    im_c = ImageCover(im)
    format_size = (120, 60)
    # result = im_c.thumbnail(format_size)
    # print(result.size)
    im_c.thumbnail(format_size)
