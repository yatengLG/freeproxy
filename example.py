# -*- coding: utf-8 -*-
# @Author  : LG

"""
随机获取单体代理
支持类型筛选
type:       指定代理类型 http,https
anonymity:  指定代理是否匿名 h(高匿),a(匿名),t(透明)
"""

import requests

data = {'type': 'http',
        'anonymity': 'h'}

c = requests.post('http://127.0.0.1:5000/get_proxy', data=data)
print(c.text)