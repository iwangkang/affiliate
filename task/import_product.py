#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-10
@description:根据已有产品xml文件将产品信息分类入库
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import urllib2

from affiliate.task.base import *
from affiliate.task.import_merchant import import_product_id_2_merchant
from affiliate.config import settings
from affiliate.lib.util.xml_util import XMLUtil
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.util.upload_util import UploadUtil
from affiliate.lib.model.pool.thread_pool import MyThreadPool
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def get_keyword_set(product, tag_dict):
    """获取关键字无重复集合"""
    keyword_set = list()
    #待分词productFeed字段
    name = product.get(tag_dict['name']).lower()
    category = product.get(tag_dict['category']).lower()
    description = product.get(tag_dict['description']).lower()
    #分词模板
    glossary = MongodbUtil.find_one('glossary')
    use_word_list = glossary.get('used')
    un_used_word_list = glossary.get('unUsed')
    for word in use_word_list:
        word = word.lower()
        if name.__contains__(word) or description.__contains__(word) or category.__contains__(word):
            keyword_set.append(word)

    wait_4_cut_word_list = [category, name, description]
    for ele in wait_4_cut_word_list.__iter__():
        for word in StringUtil.cut_word(ele):
            word = word.lower()
            if not un_used_word_list.__contains__(word) and not keyword_set.__contains__(word):
                keyword_set.append(word)
    return keyword_set


def get_product_dict(product, keyword_list, merchant_id, tag_dict):
    """拼接产品参数"""
    start_time = DateUtil.get_sys_date()
    product_dict = {
        'productId': product.get(tag_dict['id']),
        'keywordList': keyword_list,
        'productMerchantId': merchant_id,
        'productTitle': product.get(tag_dict['name']),
        'productStartTime': start_time,
        'productAliveTime': settings.alive_time,
        'productDescription': product.get(tag_dict['description']),
        'productCurrency': product.get(tag_dict['currency']),
        'productPrice': product.get(tag_dict['price']),
        'productUrl': product.get(tag_dict['url']),
        'productMpn': product.get(tag_dict.get('mpn', ''), ''),
        'productUpc': product.get(tag_dict.get('upc', ''), ''),
        'productEan': product.get(tag_dict.get('ean', ''), ''),
        'productIsbn': product.get(tag_dict.get('isbn', ''), ''),
        'productSku': product.get(tag_dict.get('sku', ''), ''),
    }
    return product_dict


def save_product_img(product, tag_dict, size):
    """下载产品图片并存入mongodb中"""
    file_name = product.get(tag_dict['image'])
    logger.info('--------------- %s' % file_name)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(file_name)
    file_body = response.read()
    file_name = UploadUtil.upload_pic(file_name, file_body, size[0], size[1])
    image = {
        'imageProductId': product.get('_id'),
        'version': DateUtil.get_sys_date(),
        'fileName': file_name,
        'imageWidth': size[0],
        'imageHeight': size[1],
    }
    image_id, update_flag = MongodbUtil.update_or_insert('image', image, {"fileName": file_name})
    if image_id:
        if update_flag:
            logger.info('Update product\'s image: %s successfully!!!' % product.get(tag_dict['image']))
        else:
            logger.info('Save product\'s image: %s successfully!!!' % product.get(tag_dict['image']))
        return image_id
    else:
        logger.info('Save product\'s image: %s failed!!!' % product.get(tag_dict['image']))
        return None


def save_keyword_index(keyword_set, product):
    """遍历keywordList更新倒排索引"""
    try:
        for keyword in keyword_set:
            existingKeyword = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
            if existingKeyword:
                if not existingKeyword['invertedIndex'].__contains__(product.get('_id').__str__()):
                    existingKeyword['invertedIndex'][product.get('_id').__str__()] = 100.0
                    status_id = MongodbUtil.save('keywordIndex', existingKeyword)
                    if status_id:
                        logger.info('Update keywordIndex: %s successfully!!!' % keyword)
                    else:
                        save_keyword_index(keyword_set, product)
                        logger.info('Try to update keywordIndex: %s again!!!' % keyword)
            else:
                keywordIndex = {
                    'keyword': keyword,
                    'invertedIndex': {product.get('_id').__str__(): 100.0},
                }
                status_id = MongodbUtil.insert('keywordIndex', keywordIndex)
                if status_id:
                    logger.info('Save keywordIndex: %s successfully!!!' % keyword)
                else:
                    save_keyword_index(keyword_set, product)
                    logger.info('Try to update keywordIndex: %s again!!!' % keyword)
    except Exception as e:
        logger.error(e.message)


def do_import_product(product, tag_dict):
    """导入商品相关信息"""
    try:
        merchant_name = product.get(tag_dict['merchant'])
        merchant = MongodbUtil.find_one('merchant', {'name': merchant_name})
        keyword_set = get_keyword_set(product, tag_dict)
        p = get_product_dict(product, keyword_set, merchant.get('_id'), tag_dict)
        #插入或更新商品
        product['_id'], update_flag = MongodbUtil.update_or_insert('product', p, {"productId": p.get('productId'), 'productMerchantId': p.get('productMerchantId')})
        if product['_id']:
            if update_flag:
                logger.info('Update product: %s successfully!!!' % p.get('productTitle'))
            else:
                logger.info('Save product: %s successfully!!!' % p.get('productTitle'))
                #遍历keywordList更新倒排索引
                save_keyword_index(keyword_set, product)
        else:
            logger.error('Save product: %s failed!!!' % p.get('productTitle'))
    except Exception as e:
        logger.error('[message: %s]; [params: %s]' % (e.message, product.__str__()))


def import_product_from_xml(file_path, tag_dict):
    """
    将指定广告xml文件导入数据库         **注意：导入前需要先人工确定商品语种、标签对应关系、和xml文件路径
    param@file_path:xml文件路径
    param@tag_dict:过滤产品标签名数组 eg:tag_dict = {'product': 'product', 'category': 'categoria',
                                                    'description', 'descricao', 'name', 'nome_produto'}

    """
    # product_pool = MyThreadPool(num_threads=512, min_pool=256, max_pool=512)
    product_pool = MyThreadPool(num_threads=1, min_pool=1, max_pool=1)
    product_list = XMLUtil.read_2_list(file_path, tag_dict['product'])
    for product in product_list:
        product_pool.add_task(do_import_product, product, tag_dict)
    product_pool.wait_completion()


def do_import_image(product, tag_dict, size):
    """导入图片相关信息"""
    try:
        exist_product = MongodbUtil.find_one('product', {'productId': product.get(tag_dict['id'])})
        if exist_product:
            #下载保存图片信息
            product['_id'] = exist_product.get('_id')
            save_product_img(product, tag_dict, size)
        else:
            logger.error('Save product\'s image: %s failed!!!' % product.get('productTitle'))
    except Exception as e:
        logger.error('[message: %s]; [params: %s]' % (e.message, product.__str__()))


def import_product_image(file_path, tag_dict):
    """下载产品图片到mongodb"""
    product_pool = MyThreadPool(num_threads=96, min_pool=64, max_pool=128)
    product_list = XMLUtil.read_2_list(file_path, tag_dict['product'])
    for product in product_list:
        for type, size in settings.image_size_list.items():
            product_pool.add_task(do_import_image, product, tag_dict, size)
    product_pool.wait_completion()


@affiliate_celery.task(ignore_result=True)
def import_product(file_path, merchant_name):
    """
    导入产品异步任务
    1.导入产品列表
    2.同步产品id到对应广告主集合中
    3.导入产品图片

    """
    import_product_from_xml(file_path, settings.tag_dict)
    import_product_id_2_merchant(merchant_name)
    import_product_image(file_path, settings.tag_dict)


if __name__ == '__main__':
    import time
    print time.time()
    for i in xrange(100000):
        word_str = 'Car  Accessories:Car Alarms & Security'
        word_arr = StringUtil.cut_word(word_str)
    print time.time()
