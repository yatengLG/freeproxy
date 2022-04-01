# -*- coding: utf-8 -*-
# @Author  : LG


from core.spider import SpiderBC
import requests
from bs4 import BeautifulSoup


class Ip3366(SpiderBC):
    def __init__(self):
        super(Ip3366, self).__init__()
        self.base_url = 'http://www.ip3366.net/free/?page=1'

    def get_proxys(self):
        results = []
        response = requests.get(self.base_url, headers=self.headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            tbody = soup.find('table').find('tbody')
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                tds = [td.text for td in tds]
                r = {'type': tds[3].lower(), 'host': tds[0], 'port':tds[1]}
                results.append(r)
        return results


if __name__ == '__main__':
    ip3366 = Ip3366()
    r = ip3366.get_proxys()
    print(r)
