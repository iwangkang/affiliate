#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-20
@description:MongoDB工具类
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from cStringIO import StringIO
from bson.objectid import ObjectId

from affiliate.lib.model.mongod.base import Base
from affiliate.lib.util.logger_util import logger


class MongodbUtil(Base):
    """
    MongoDB工具类

    """

    @classmethod
    def put(cls, filename, image, suffix='png'):
        """上传文件"""
        try:
            filename = '%s.%s' % (filename, suffix)
            data = None
            headers = {
                "Cache-Control": "max-age=%s" % (60 * 60 * 24),
                "Content-type": "image/%s" % suffix
            }
            params = {
                "filename": filename,
                "headers": headers,
                "suffix": suffix
            }
            data = StringIO()
            image.save(data, suffix)
            cls.fs.put(data.getvalue(), **params)
            return filename
        except Exception as e:
            logger.error(e.message)
        finally:
            data.close()

    @classmethod
    def get(cls, filename=None, object_id=None):
        """取文件"""
        try:
            assert filename or object_id
            content_obj = cls.fs.get_last_version(filename) if filename else cls.fs.get(ObjectId(object_id))
            content = content_obj.read()
            headers = content_obj.headers
            filename = content_obj.filename
            return {"file": content, "headers": headers, "filename": filename}
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def list_fs(cls):
        """获得文件列表"""
        try:
            file_list = cls.fs.list()
            return file_list
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def remove(cls, filename=None, object_id=None):
        """删除文件"""
        try:
            assert filename or object_id
            key = cls.fs.get_last_version(filename)._id if filename else ObjectId(object_id)
            cls.fs.delete(key)
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def insert(cls, db, collection, document):
        """插入数据"""
        try:
            if not document:
                return None
            obj_id = cls.client[db][collection].insert(document)
            return obj_id
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def update_or_insert(cls, db, collection, document, spec_or_id=None):
        """更新数据，如果数据不存在则插入"""
        try:
            update_flag = False
            if (isinstance(spec_or_id, str) or isinstance(spec_or_id, dict)) and spec_or_id:
                existing_document = cls.find_one(db, collection, spec_or_id)
                if not existing_document:
                    obj_id = cls.insert(db, collection, document)
                else:
                    for k, v in document.items():
                        existing_document[k] = v
                    obj_id = cls.client[db][collection].save(existing_document)
                    update_flag = True
            else:
                obj_id = cls.insert(db, collection, document)
            return obj_id, update_flag
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def save(cls, db, collection, document):
        """保存更新数据"""
        try:
            if not document:
                return None
            obj_id = cls.client[db][collection].save(document)
            return obj_id
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def update(cls, db, collection, spec_or_id, document):
        """保存更新数据"""
        try:
            if not document:
                return None
            obj_id = cls.client[db][collection].update(spec_or_id, document)
            return obj_id
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def find_one(cls, db, collection, spec_or_id=None):
        """根据id或者特殊匹配查询mongodb"""
        try:
            if isinstance(spec_or_id, str):
                id = ObjectId(spec_or_id)
                result = cls.client[db][collection].find_one(id)
                return result
            result = cls.client[db][collection].find_one(spec_or_id)
            return result
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def find(cls, db, collection, spec_or_id=None, skip=0, limit=0, sort=None):
        """获取指定集合所有数据"""
        try:
            if limit:
                if sort:
                    obj_list = cls.client[db][collection].find(spec_or_id).skip(skip).limit(limit).sort(sort)
                else:
                    obj_list = cls.client[db][collection].find(spec_or_id).skip(skip).limit(limit)
            else:
                if sort:
                    obj_list = cls.client[db][collection].find(spec_or_id).sort(sort)
                else:
                    obj_list = cls.client[db][collection].find(spec_or_id)
            return list(obj_list)
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def delete(cls, db, collection, spec_or_id=None):
        """删除集合数据"""
        try:
            result = cls.client[db][collection].remove(spec_or_id)
            return result
        except Exception as e:
            logger.error(e.message)

    @classmethod
    def group(cls, db, collection, key, condition=None, initial=list(), reduce=None):
        """
        分组查询数据
        param@key:根据key指定的字段进行分组
        param@condition:筛选条件
        param@initial:对于一组中的各个记录，都作为reduce函数的第一个参数执行reduce函数
        param@reduce:reduce函数引用

        """
        try:
            result = cls.client[db][collection].group(key=key, condition=condition, initial=initial, reduce=reduce)
            return result
        except Exception as e:
            logger.error(e.message)


if __name__ == '__main__':
    result = MongodbUtil.find_one('shopping', 'category')
    print len(list(result))