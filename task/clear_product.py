#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-12-31
@description:清理过期产品
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from affiliate.task.base import *
from affiliate.lib.util.date_util import DateUtil
from affiliate.lib.model.mongod.mongodb_util import MongodbUtil


def delete_product(product):
    """删除产品及产品相关信息"""
    product_id = product.get('_id')
    MongodbUtil.delete('shopping', 'product', product)
    logger.info('Delete a product: %s successfully!!!' % product.get('title'))
    #删除索引中product.id
    keyword_list = product.get('keywordList')
    for keyword in keyword_list:
        keyword = MongodbUtil.find_one('shopping', 'keywordIndex', {'keyword': keyword})
        if not keyword:
            continue
        if keyword['invertedIndex'].__contains__(product_id.__str__()):
            del keyword['invertedIndex'][product_id.__str__()]
            MongodbUtil.save('shopping', 'keywordIndex', keyword)
            logger.info('Update keyword index: %s successfully!!!' % keyword.get('keyword'))
        #删除merchant中product.id
    merchant_id = product.get('merchantId')
    merchant = MongodbUtil.find_one('shopping', 'merchant', {'_id': merchant_id})
    index_id = merchant['productIdList'].index(product_id)
    if isinstance(index_id, int):
        del merchant['productIdList'][index_id]
    MongodbUtil.save('shopping', 'merchant', merchant)
    logger.info('Update merchant productIdList successfully!!!')
    #删除product的image及图片文件
    images = MongodbUtil.find('shopping', 'image', {'productId': product_id})
    for image in images:
        MongodbUtil.remove(filename=image.get('fileName'))
    MongodbUtil.delete('shopping', 'image', {'productId': product_id})


def save_overdue_product(product_list):
    """保存过期产品到overdueProduct集合中"""
    update_count = 0
    insert_count = 0
    for product in product_list:
        product_id = product.get('_id')
        overdue_product_id = MongodbUtil.insert('shopping', 'overdueProduct', product)
        if overdue_product_id:
            insert_count += 1
            logger.info('Insert overdue product: %s successfully!!!' % product.get('title'))
            #cpc统计数据转移至备份集合overdueCpc中后删除
        cpc_list = MongodbUtil.find('shopping', 'cpc', {'productId': product_id})
        save_overdue_cpc(overdue_product_id, product, cpc_list)
        MongodbUtil.delete('shopping', 'cpc', {'cpcProductId': product_id})
    logger.info('Update %s overdue product, Insert %s overdue product!!!' % (update_count, insert_count))


def save_overdue_cpc(overdue_product_id, product, cpc_list):
    """定期备份cpc跟踪点击数到overdueCpc集合中"""
    for cpc in cpc_list:
        overdue_cpc = {
            'cpcOverdueProductId': overdue_product_id,
            'webmaster': cpc.get('webmaster'),
            'merchant': cpc.get('merchant'),
            'adPositionId': cpc.get('adPositionId'),
            'clickTime': cpc.get('clickTime'),
            'clearTime': DateUtil.get_sys_time(),
            'takeEffect': cpc.get('takeEffect'),
        }
        overdue_cpc_id = MongodbUtil.insert('shopping', 'overdueCpc', overdue_cpc)
        if overdue_cpc_id:
            logger.info('Insert overdue cpc from:%s to:%s successfully!!!' % (
            overdue_cpc.get('webmaster'), overdue_cpc.get('merchant')))


def clear_product():
    """清理过期产品到备份集合中"""
    try:
        product_list = MongodbUtil.find('shopping', 'product')
        overdue_product_list = list()
        today = DateUtil.get_sys_date()
        for product in product_list.__iter__():
            start_date = product.get('startTime')
            alive_time = product.get('aliveTime')
            end_date = DateUtil.get_end_date(start_date, alive_time)
            if today > end_date:
                #添加到备份产品集合
                overdue_product_list.append(product)
                #执行删除操作
                delete_product(product)
        save_overdue_product(overdue_product_list)
    except Exception as e:
        logger.error(e.message)


if __name__ == '__main__':
    today = DateUtil.get_sys_date()
    start_date = '2014-02-18'
    alive_time = 30
    end_date = DateUtil.get_end_date(start_date, alive_time)
    print end_date
    print today > end_date
