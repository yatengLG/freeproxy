# -*- coding: utf-8 -*-
# @Author  : LG

from core.spider import SpiderBC
import requests


class ProxyLists(SpiderBC):
    def __init__(self):
        super(ProxyLists, self).__init__()
        self.base_url = 'http://www.proxylists.net/{}'

    def get_proxys(self):
        results = []
        response = requests.get(self.base_url.format('http_highanon.txt'), headers=self.headers)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                line = line.rstrip('\r\t\n')
                if line:
                    host, port = line.split(':')
                    if ''.join(host.split('.')).isnumeric():
                        r = {'type': 'http', 'host': host, 'port':port}
                        results.append(r)

        response = requests.get(self.base_url.format('http.txt'), headers=self.headers)
        if response.status_code == 200:
            for line in response.text.split('\n'):
                line = line.rstrip('\r\t\n')
                if line:
                    host, port = line.split(':')
                    if ''.join(host.split('.')).isnumeric():
                        r = {'type': 'http', 'host': host, 'port':port}
                        results.append(r)


        return results


if __name__ == '__main__':
    proxylists = ProxyLists()
    proxys = proxylists.get_proxys()
    print(proxys)