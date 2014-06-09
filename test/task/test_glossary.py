#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-3
@description:词汇表测试
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.import_glossary import import_glossary, replenish_glossary


def test_import_glossary():
    import_glossary()


def test_replenish_glossary(file_path):
    replenish_glossary(file_path, 'categoria')


if __name__ == '__main__':
    #导入并补充glossary
    test_import_glossary()

    # #补充glossary['used']
    # test_replenish_glossary('D:/shopbot.xml')