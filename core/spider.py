# -*- coding: utf-8 -*-
# @Author  : LG

from typing import List, Dict


class SpiderBC:
    def __init__(self):
        self.base_url = None
        self.num = None
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}

    def get_proxys(self) -> List[Dict]:
        raise NotImplementedError


