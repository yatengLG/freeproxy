# -*- coding: utf-8 -*-
# @Author  : LG

from core.spider import SpiderBC
import requests


class PubProxy(SpiderBC):
    def __init__(self):
        super(PubProxy, self).__init__()
        self.base_url = "http://pubproxy.com/api/proxy?limit=5&format=txt&type=http"

    def get_proxys(self):
        results = []
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                line = line.rstrip('\r\t\n')
                if line:
                    host, port = line.split(':')
                    r = {'type': 'http', 'host': host, 'port':port}
                    results.append(r)
        return results


if __name__ == '__main__':
    pubproxys = PubProxy()
    proxys = pubproxys.get_proxys()
    print(proxys)
