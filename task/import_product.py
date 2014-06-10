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
from affiliate.lib.util.math_util import MathUtil
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.util.upload_util import UploadUtil
from affiliate.lib.model.pool.thread_pool import MyThreadPool
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def get_keyword_set(product, tag_dict):
    """获取关键字无重复集合"""
    keyword_set = list()
    #待分词productFeed字段
    name = product.get(tag_dict['name']).lower() if product.get(tag_dict['name']) else ''
    category = product.get(tag_dict['category']).lower() if product.get(tag_dict['category']) else ''
    description = product.get(tag_dict['description']).lower() if product.get(tag_dict['description']).lower() else ''
    #分词模板
    glossary = MongodbUtil.find_one('shopping', 'glossary')
    use_word_list = glossary.get('used')
    un_used_word_list = glossary.get('unUsed')
    for word in use_word_list:
        word = word.lower()
        if name.__contains__(word) or description.__contains__(word) or category.__contains__(word):
            keyword_set.append(word)

    wait_4_cut_word_list = [category, name, description]
    for ele in wait_4_cut_word_list.__iter__():
        if not ele:
            continue
        for word in StringUtil.cut_word(ele):
            word = word.lower()
            if not un_used_word_list.__contains__(word) and not keyword_set.__contains__(word):
                keyword_set.append(word)
    return keyword_set


def fill_category_dict(category_list, category_result, category, name, description):
    """补充类别关键词"""
    c_k = category_list[category_result].get('category_keyword')
    d_k = category_list[category_result].get('desc_keyword')
    n_k = category_list[category_result].get('name_keyword')
    c_k_list = StringUtil.cut_word(category) if category else list()
    d_k_list = StringUtil.cut_word(description) if description else list()
    n_k_list = StringUtil.cut_word(name) if name else list()
    for keyword in c_k_list:
        if not c_k.__contains__(keyword):
            c_k.append(keyword)
        if d_k.__contains__(keyword):
            d_k.remove(keyword)
        if n_k.__contains__(keyword):
            n_k.remove(keyword)
    for keyword in d_k_list:
        if not d_k.__contains__(keyword) and not c_k.__contains__(keyword):
            d_k.append(keyword)
        if n_k.__contains__(keyword):
            n_k.remove(keyword)
    for keyword in n_k_list:
        if not n_k.__contains__(keyword) and not d_k.__contains__(keyword) and not c_k.__contains__(keyword):
            n_k.append(keyword)
    category_list[category_result]['category_keyword'] = c_k
    category_list[category_result]['desc_keyword'] = d_k
    category_list[category_result]['name_keyword'] = n_k
    MongodbUtil.update('shopping', 'category', {'_id': category_list.get('_id')}, category_list)


def fit_category(category_list, category, name, description):
    """根据类别关键词定类"""
    percentage = 0.0
    category_result = 'Others'
    category_keyword_list = StringUtil.cut_word(category) if category else list()
    name_keyword_list = StringUtil.cut_word(name) if name else list()
    desc_keyword_list = StringUtil.cut_word(description) if description else list()
    total_count = len(category_keyword_list) + len(name_keyword_list) + len(desc_keyword_list)
    for c, k_dict in category_list.items():
        grade = 0.0
        for keyword in category_keyword_list:
            if k_dict['category_keyword'].__contains__(keyword):
                grade += settings.category_grade
        for keyword in name_keyword_list:
            if k_dict['desc_keyword'].__contains__(keyword):
                grade += settings.desc_grade
        for keyword in desc_keyword_list:
            if k_dict['name_keyword'].__contains__(keyword):
                grade += settings.name_grade

        new_percentage = float(grade) / float(total_count)
        if percentage < new_percentage:
            category_result = c
            percentage = new_percentage
    return category_result


def get_product_dict(product, keyword_list, merchant_id, tag_dict):
    """拼接产品参数"""
    start_time = DateUtil.get_sys_date()
    category_mode = MongodbUtil.find_one('shopping', 'category')
    category_list, category, name, description = category_mode.get('category_dict'), product.get(tag_dict['category']), product.get(tag_dict['name']), product.get(tag_dict['description'])
    # 商品匹配定类
    category_result = fit_category(category_list, category, name, description)
    # 填充类别关键词集合
    fill_category_dict(category_list, category_result, category, name, description)
    product_dict = {
        'productId': product.get(tag_dict['id']),
        'category': category_result,
        'keywordList': keyword_list,
        'merchantId': merchant_id,
        'title': str(product.get(tag_dict['name'])).replace('&', ' '),
        'startTime': start_time,
        'aliveTime': settings.alive_time,
        'description': str(product.get(tag_dict['description'])).replace('&', ''),
        'currency': product.get(tag_dict['currency']),
        'price': float(product.get(tag_dict['price'])),
        'url': product.get(tag_dict['url']),
        'mpn': product.get(tag_dict.get('mpn', ''), ''),
        'color': product.get(tag_dict.get('color', ''), ''),
        'size': product.get(tag_dict.get('size', ''), ''),
        'merchantCategory': product.get(tag_dict.get('merchantCategory', ''), ''),
        'availability': product.get(tag_dict.get('availability', ''), ''),
        'shippingWeight': product.get(tag_dict.get('shippingWeight', ''), ''),
        'gender': product.get(tag_dict.get('gender', ''), ''),
        'ageGroup': product.get(tag_dict.get('ageGroup', ''), ''),
    }
    return product_dict


def save_product_img(product, tag_dict, size):
    """下载产品图片并存入mongodb中"""
    file_name = product.get(tag_dict['image'])
    opener = urllib2.build_opener()
    response = opener.open(file_name)
    file_body = response.read()
    file_name = UploadUtil.upload_pic(file_name, file_body, size[0], size[1])
    image = {
        'productId': product.get('_id'),
        'version': DateUtil.get_sys_time(),
        'fileName': file_name,
        'width': size[0],
        'height': size[1],
    }
    image_id = MongodbUtil.insert('shopping', 'image', image)
    if image_id:
        logger.info('Save product\'s image: %s successfully!!!' % product.get(tag_dict['image']))
        return image_id
    else:
        logger.info('Save product\'s image: %s failed!!!' % product.get(tag_dict['image']))
        return None


def save_keyword_index(keyword_set, product):
    """遍历keywordList更新倒排索引"""
    try:
        for keyword in keyword_set:
            existingKeyword = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword})
            if existingKeyword:
                if not existingKeyword['invertedIndex'].__contains__(product.get('_id').__str__()):
                    existingKeyword['invertedIndex'][product.get('_id').__str__()] = 100.0
                    status_id = MongodbUtil.save('shopping', 'keywordIndex', existingKeyword)
                    if status_id:
                        logger.info('Update keywordIndex: %s successfully!!!' % keyword)
                    else:
                        save_keyword_index(keyword_set, product)
                        logger.info('Try to update keywordIndex: %s again!!!' % keyword)
            else:
                keywordIndex = {
                    'keyword': keyword,
                    'searchTimes': 0,
                    'invertedIndex': {product.get('_id').__str__(): 100.0},
                }
                status_id = MongodbUtil.insert('shopping', 'keywordIndex', keywordIndex)
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
        merchant_list = get_merchant_list()
        if merchant_name not in merchant_list:
            return
        merchant = MongodbUtil.find_one('shopping', 'merchant', {'name': merchant_name})
        keyword_set = get_keyword_set(product, tag_dict)
        p = get_product_dict(product, keyword_set, merchant.get('_id'), tag_dict)
        # 插入或更新商品
        product['_id'], update_flag = MongodbUtil.update_or_insert('shopping', 'product', p, {"productId": p.get('productId'), 'merchantId': p.get('merchantId')})
        if product['_id']:
            if update_flag:
                logger.info('Update product: %s successfully!!!' % p.get('title'))
            else:
                logger.info('Save product: %s successfully!!!' % p.get('title'))
                # 遍历keywordList更新倒排索引
                save_keyword_index(keyword_set, product)
                # 下载产品图片
                for type, size in settings.image_size_list.items():
                    do_import_image(product, tag_dict, size)
        else:
            logger.error('Save product: %s failed!!!' % p.get('title'))
    except Exception as e:
        logger.error('[message: %s]; [params: %s]' % (e.message, product.__str__()))


def do_import_image(product, tag_dict, size):
    """导入图片相关信息"""
    try:
        exist_product = MongodbUtil.find_one('shopping', 'product', {'productId': product.get(tag_dict['id'])})
        if exist_product:
            #下载保存图片信息
            product['_id'] = exist_product.get('_id')
            save_product_img(product, tag_dict, size)
        else:
            logger.info('Save product\'s image: %s failed!!!' % product.get('title'))
    except Exception as e:
        logger.error('[message: %s]; [params: %s]' % (e.message, product.__str__()))


def check_useful(product, tag_dict):
    """检查产品feed提供的信息是否可用"""
    try:
        # check merchant
        check_status = False
        merchant_name = product.get(tag_dict['merchant'])
        merchant_list = get_merchant_list()
        if merchant_name not in merchant_list:
            return check_status
        # checking that wheather the image is available
        img_url = product.get(tag_dict['image'])
        opener = urllib2.build_opener()
        response = opener.open(img_url)
        file_body = response.read()
        if file_body:
            check_status = True
        return check_status
    except Exception as e:
        logger.error('Check upload img error: %s' % e.message)
        return check_status


def import_product_from_xml(file_path, tag_dict):
    """
    将指定广告xml文件导入数据库         **注意：导入前需要先人工确定商品语种、标签对应关系、和xml文件路径
    param@file_path:xml文件路径
    param@tag_dict:过滤产品标签名数组 eg:tag_dict = {'product': 'product', 'category': 'categoria',
                                                    'description', 'descricao', 'name', 'nome_produto'}

    """
    try:
        product_pool = MyThreadPool(num_threads=1, min_pool=1, max_pool=1)
        product_list = XMLUtil.read_2_list(file_path, tag_dict['product'])
        for product in product_list:
            # if check_useful(product, settings.tag_dict):
            product_pool.add_task(do_import_product, product, tag_dict)
        product_pool.wait_completion()
    except Exception as e:
        logger.error('Import product from xml file error: %s' % e.message)


@affiliate_celery.task(ignore_result=True)
def import_product(file_path, merchant_name):
    """
    导入产品异步任务
    1.导入产品相关信息
    2.同步产品id到对应广告主集合中

    """
    try:
        product_list = XMLUtil.read_2_list(file_path, settings.tag_dict['product'])
        for product in product_list:
            if check_useful(product, settings.tag_dict):
                do_import_product(product, settings.tag_dict)
        import_product_id_2_merchant(merchant_name)
    except Exception as e:
        logger.error('Import product error: %s' % e.message)


if __name__ == '__main__':
    pass