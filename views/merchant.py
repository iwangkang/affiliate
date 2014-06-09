#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:广告主逻辑层
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import ast

from bson.objectid import ObjectId

from affiliate.config import settings
from affiliate.config.celeryconfig import affiliate_celery
from affiliate.views.base import BaseHandler
from affiliate.lib.util.logger_util import logger
from affiliate.lib.util.xml_util import XMLUtil
from affiliate.lib.util.check_util import CheckUtil
from affiliate.lib.util.file_util import FileUtil
from affiliate.lib.util.string_util import StringUtil
from affiliate.lib.model.models.models import MongodbUtil
from affiliate.lib.model.models.models import PageResponse, BrokenResponse, SuccessfulResponse


class ManageProductHandler(BaseHandler):
    """
    广告主商品管理

    """

    def on_request(self):
        try:
            #身份验证
            check_auth = CheckUtil.check_auth(**self.params)
            if check_auth:
                method_name = self.params.get('method')
                method_dict = {
                    'search': lambda: self.search_product(**self.params),
                    'modify': lambda: self.modify_product(**self.params),
                    'delete': lambda: self.delete_product(**self.params),
                    'import': lambda: self.import_product(**self.params),
                }
                method_dict[method_name]()
            else:
                logger.warning('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                    'Check failed', self.request.host, self.request.remote_ip, self.params.__str__()))
                error_response = BrokenResponse()
                self._jsonify_response(error_response)
        except Exception as e:
            logger.warning('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                e.message, self.request.host, self.request.remote_ip, self.params.__str__()))
            error_response = BrokenResponse()
            self._jsonify_response(error_response)

    def import_product(self, **kwargs):
        """导入商品"""
        self._event('import')
        #获取xml文件信息
        file_name = self.request.files['product_file'][0]['filename']
        file_body = self.request.files['product_file'][0]['body']
        if not self.check_file(file_name, file_body):
            logger.warning('[message: %s]; [host: %s]; [ip: %s]; [params: %s]' % (
                'Check failed', self.request.host, self.request.remote_ip, self.params.__str__()))
            error_response = BrokenResponse()
            self._jsonify_response(error_response)
        # 将xml文件保存
        file_name = FileUtil.get_filename_by_date('.xml')
        merchant_name = kwargs.get('merchant')
        file_path = '%s/productFeeds/%s/' % (settings.files_dir, merchant_name)
        file_path = FileUtil.write_2_file(file_path, file_name, file_body, 'utf-8')
        # 异步导入商品列表
        affiliate_celery.send_task('affiliate.task.import_product.import_product', args=(file_path, merchant_name))
        successful_response = SuccessfulResponse()
        self._jsonify_response(successful_response)

    def delete_product(self, **kwargs):
        """删除商品"""
        self._event('delete')
        product_id_list = StringUtil.str_2_list(kwargs.get('productIdList'))
        merchant = MongodbUtil.find_one('merchant', {'name': kwargs.get('merchant')})
        for product_id in product_id_list:
            product = MongodbUtil.find_one('product', {
                'productId': product_id,
                'productMerchantId': merchant.get('_id')
            })
            if not product:
                continue
            # 删除广告主中的商品id
            idx = merchant['productIdList'].index(product.get('_id'))
            del merchant['productIdList'][idx]
            MongodbUtil.save('merchant', merchant)
            # 删除倒排索引中的商品id
            keyword_list = product.get('keywordList')
            for keyword in keyword_list:
                existingKeyword = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
                if existingKeyword:
                    self.del_keyword_index(keyword, product.get('_id'))
            # 删除商品
            MongodbUtil.delete('product', {
                'productId': product_id,
                'productMerchantId': merchant.get('_id')
            })
            logger.info('Delete %s\'s product: %s successfully!!!' % (kwargs.get('merchant'), product_id))
        successful_response = SuccessfulResponse()
        self._jsonify_response(successful_response)

    def modify_product(self, **kwargs):
        """商品修改"""
        self._event('modify')
        product = ast.literal_eval(kwargs.get('product'))
        exists_product = MongodbUtil.find_one('product', {
            'productId': product.get('productId'),
            'productMerchantId': ObjectId(product.get('productMerchantId'))
        })
        #获取更新前关键词列表 删除倒排索引中的商品id
        keyword_list_old = exists_product.get('keywordList')
        keyword_list_new = product.get('keywordList')
        for keyword in keyword_list_old:
            if keyword not in keyword_list_new:
                self.del_keyword_index(keyword, exists_product.get('_id'))
        #新增倒排索引中的商品id
        append_keyword_list = list()
        for keyword in keyword_list_new:
            if keyword not in keyword_list_old:
                if keyword:
                    append_keyword_list.append(keyword)
        self.save_keyword_index(append_keyword_list, exists_product.get('_id'))
        #只允许修改keywordList
        for k, v in product.items():
            if k != 'keywordList':
                continue
            exists_product[k] = v
        # for k, v in product.items():
        #     if k == 'productMerchantId':
        #         exists_product[k] = ObjectId(product.get('productMerchantId'))
        #         continue
        #     exists_product[k] = v
        MongodbUtil.save('product', exists_product)

        successful_response = SuccessfulResponse()
        self._jsonify_response(successful_response)

    def search_product(self, **kwargs):
        """查询产品列表"""
        self._event('search')
        merchant = MongodbUtil.find_one('merchant', {'name': kwargs.get('merchant')})
        product_id_list = merchant.get('productIdList')
        page_response = PageResponse(product_id_list, **kwargs)
        self._jsonify_response(page_response)

    def del_keyword_index(self, keyword, product_id):
        """删除倒排索引中的商品id"""
        existingKeyword = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
        if existingKeyword:
            p_str_id = product_id.__str__()
            if existingKeyword.get('invertedIndex').__contains__(p_str_id):
                del existingKeyword['invertedIndex'][p_str_id]
                status_id = MongodbUtil.save('keywordIndex', existingKeyword)
                if status_id:
                    logger.info('Update keyword: %s successfully!!!' % keyword)
                else:
                    logger.info('Update keyword: %s failed!!!' % keyword)

    def check_file(self, file_name, file_body):
        """检查文件是否符合规范要求"""
        try:
            check_status = False
            if not (file_name.index('.xml') + 4) == len(file_name):
                return check_status
            product_list = XMLUtil.read_2_list_by_string(file_body, 'product')
            product = product_list.pop()
            for k, v in product.items():
                if settings.tag_dict.__contains__(k):
                    continue
                return check_status
            check_status = True
            return check_status
        except Exception:
            return check_status

    def save_keyword_index(self, keyword_set, product_id):
        """遍历keywordList更新倒排索引"""
        for keyword in keyword_set:
            existingKeyword = MongodbUtil.find_one('keywordIndex', {'keyword': keyword})
            if existingKeyword:
                if not existingKeyword['invertedIndex'].__contains__(product_id.__str__()):
                    existingKeyword['invertedIndex'][product_id.__str__()] = 100.0
                    status_id = MongodbUtil.save('keywordIndex', existingKeyword)
                    if status_id:
                        logger.info('Update keywordIndex: %s successfully!!!' % keyword)
                    else:
                        self.save_keyword_index(keyword_set, product_id)
                        logger.info('Try to update keywordIndex: %s again!!!' % keyword)
            else:
                keywordIndex = {
                    'keyword': keyword,
                    'invertedIndex': {product_id.__str__(): 100.0},
                }
                status_id = MongodbUtil.insert('keywordIndex', keywordIndex)
                if status_id:
                    logger.info('Save keywordIndex: %s successfully!!!' % keyword)
                else:
                    self.save_keyword_index(keyword_set, product_id)
                    logger.info('Try to update keywordIndex: %s again!!!' % keyword)














