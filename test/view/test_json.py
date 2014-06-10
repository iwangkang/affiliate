#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:14-5-19
@description:
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import ujson as json


order_info = """
{
    "orderId": " EA10669853226",
    "orderTime": "2014-5-19 10:21:58",
    "productList": [
        {
            "name": "iphone",
            "currency": "USD",
            "singlePrice": 3.9,
            "totalPrice": 7.8,
            "productCount": 2,
            "category": "3C",
            "merchant": "thinkcart",
        },
        {
            "name": "ipad",
            "currency": "USD",
            "singlePrice": 3.9,
            "totalPrice": 7.8,
            "productCount": 2,
            "category": "3C",
            "merchant": "thinkcart",
        }
    ]
}
"""

if __name__ == '__main__':
    order = json.loads(order_info)
    print type(order)
    # product_list = order.get('productList')
    # for product in product_list:
    #     print product.get('name')