#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-10
@description:xml工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


class XMLUtil(object):
    """
    xml解析工具类

    """

    @classmethod
    def read_2_list(cls, file_path, tag_name):
        """
        读取指定xml文件内容，并将xml转化为tree对象进行迭代，转化为list<object>返回

        """
        tree = ET.ElementTree(file=file_path)
        root = tree.getroot()
        children = root.iter(tag_name)
        obj_list = list()
        for child in children:
            obj = dict()
            for attr in child.iter():
                obj[attr.tag] = attr.text
            obj_list.append(obj)
        return obj_list

    @classmethod
    def read_2_list_by_string(cls, xml_str, tag_name):
        """
        根据xml字符串转化为tree对象进行迭代，转化为list<object>返回

        """
        tree = ET.ElementTree(ET.fromstring(xml_str))
        root = tree.getroot()
        children = root.iter(tag_name)
        obj_list = list()
        for child in children:
            obj = dict()
            for attr in child.iter():
                obj[attr.tag] = attr.text
            obj_list.append(obj)
        return obj_list

    @classmethod
    def get_obj_set(cls, obj_list=None):
        """
        获取无重复value值的集合

        """
        if not obj_list:
            return None
        obj_set = list()
        for obj in obj_list.__iter__():
            if not obj in obj_set:
                obj_set.append(obj)
        return obj_set

    @classmethod
    def get_root(cls, file_path):
        """
        读取指定xml文件内容，并将xml转化为tree对象
        field@file_path: xml文件路径
        field@return: xml根节点Element实例对象

        """
        tree = ET.ElementTree(file=file_path)
        root = tree.getroot()
        return root


if __name__ == '__main__':
    obj_list = XMLUtil.read_2_list('D:/test.xml', 'product')
    print(obj_list.__len__())
    for obj in obj_list.__iter__():
        print obj.get('categoria')
        # category_name = XMLUtil.get_attribute(obj, 'categoria')
        # print category_name
