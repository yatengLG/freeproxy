# -*- coding: utf-8 -*-
# @Author  : LG

from core.spider import SpiderBC
import requests
from json import loads


class FateZero(SpiderBC):
    def __init__(self):
        super(FateZero, self).__init__()
        self.base_url = 'http://proxylist.fatezero.org/proxy.list'

    def get_proxys(self):
        results = []
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                if line:
                    line = loads(line)
                    r = {'type':line['type'], 'host': line['host'], 'port':line['port'], 'address':line['country']}
                    if line['anonymity'] == 'high_anonymous':
                        r['anonymity'] = 'h'
                    elif line['anonymity'] == 'anonymous':
                        r['anonymity'] = 'a'
                    elif line['anonymity'] == 'transparent':
                        r['anonymity'] = 't'
                    else:
                        r['anonymity'] = ''
                    results.append(r)
        return results


if __name__ == '__main__':
    FZ = FateZero()
    proxys = FZ.get_proxys()
    print(proxys)