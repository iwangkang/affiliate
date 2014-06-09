#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:默认配置信息
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

PROCESS = 1
PORT = 5000
PORT_GROUP = None

# HOST SRC
HOST_SRC = 'http://affiliate.xingcloud.com'

# ROUTING PATH TEMPLATE
INDEX_TEMPLATE = 'index.html'
ERROR_TEMPLATE = 'error.html'
OFFLINE_TEMPLATE = 'offline.html'
UPLOAD_TEMPLATE = 'merchant/upload.html'
INDEX_TEMPLATE_MERCHANT = 'merchant/index.html'
INDEX_TEMPLATE_WEBMASTER = 'webmaster/index.html'

# EMAIL LOGGER
LOG_MAILHOST = 'smtp.exmail.qq.com:25'
LOG_FROM = 'wangkang@xingcloud.com'
LOG_TO = ('1228202366@qq.com', )
LOG_SUBJECT = 'Email for affiliate error.'
LOG_CREDENTIAL = ('wangkang@xingcloud.com', '123456')

# PAGINATION
PAGE_SIZE = 10

# TASK IMPORT PRODUCT
ALIVE_TIME = 30
UPLOAD_MAX_SIZE = 1024*1024*30
IMAGE_SIZE_LIST = {
    'small': (128, 128),
    'middle': (210, 210),
    'big': (337, 337),
}

# THREAD POOL
DEFAULT_MIN_POOL = 10
DEFAULT_MAX_POOL = 64

# PRODUCT FEEDS TAG
TAG_DICT = {
    'product': 'product',
    'merchant': 'merchant',
    'id': 'id',
    'name': 'name',
    'url': 'url',
    'description': 'description',
    'image': 'image',
    'currency': 'currency',
    'price': 'price',
    'category': 'category',
    'mpn': 'mpn',
    'upc': 'upc',
    'ean': 'ean',
    'isbn': 'isbn',
    'sku': 'sku',
}

# TAG_DICT = {
#     'product': 'product',
#     'merchant': 'marca',
#     'id': 'id',
#     'name': 'nome_produto',
#     'url': 'url',
#     'description': 'descricao',
#     'image': 'imagem',
#     'currency': 'currency',
#     'price': 'preco',
#     'category': 'categoria',
#     'mpn': 'mpn',
# }

# 切词分隔符 & 需要替换转义的无用字符       注释：会根据xml文件不断地迭代更新
WORD_SEPARATOR = [':', ' ', '/']
WORD_REPLACE = {
    '(': '', ')': '',
    '&amp;': '&', '.': '',
    ',': '', ':': '',
    '"': '', '<br>': '',
    '”':'', '‘': '\'',
    '<br />': '', '&nbsp;': ' ',
    '°': '', '℉': '',
    '℃': '', '`': '',
    '＊': '*', '\n': '',
    'α': '', '/>': '',
    '<br': '', '>': '',
    '\'\'': '', '#': '',
    '–': '', 'ω': '',
    '“': '', '￠': '',
    '%': '', '~': '',
    'φ': '', '?': '',
    '≤':'', '-': '',
    '&': '',
}