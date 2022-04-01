# -*- coding: utf-8 -*-
# @Author  : LG

import time
import requests
from json import loads


class Checker:
    def __init__(self, logger=None):
        self.check_url_format = '{}://httpbin.org/get?show_env=1&current={}'
        self.origin_ip = None
        self.logger = logger

        self._get_origin_ip()

    def _get_origin_ip(self):
        try:
            response = requests.get(self.check_url_format.format('http', ''))
            if response.status_code == 200:
                ips = loads(response.text)['origin']
                self.origin_ip = ips
        except:
            return

    def check(self, type:str, host:str, port:str, timeout:int=5):
        result = {}
        try:
            response = requests.get(self.check_url_format.format(type, time.time()),
                                    proxies={type: "//{}:{}".format(host, port)},
                                    timeout=timeout)
            if response.status_code == 200:
                response = loads(response.text)

                current_time = float(response.get('args', {}).get('current', 0))
                if current_time != 0:
                    result['cost_time'] = time.time() - current_time

                if self.origin_ip in response.get('origin', ''):
                    result['anonymity'] = 't'
                elif response.get('headers', {}).get('Via', ''):
                    result['anonymity'] = 'a'
                else:
                    result['anonymity'] = 'h'

                result['type'] = type
                result['host'] = host
                result['port'] = port
            return result

        except Exception as e:
            if self.logger is not None:
                self.logger.debug('{}'.format(e))
        return False


if __name__ == '__main__':
    C = Checker()
    r = C.check('http', '112.250.107.37', '53281', timeout=5)
    print(r)

