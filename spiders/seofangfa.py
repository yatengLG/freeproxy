# -*- coding: utf-8 -*-
# @Author  : LG

from core.spider import SpiderBC
import requests
from bs4 import BeautifulSoup


class SeoFangFa(SpiderBC):
    def __init__(self):
        super(SeoFangFa, self).__init__()
        self.base_url = 'https://proxy.seofangfa.com/'

    def get_proxys(self):
        results = []
        response = requests.get(self.base_url, headers=self.headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find('table', {'class': 'table'})
            tb = table.find('tbody')
            trs = tb.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                tds = [td.text for td in tds]
                r = {'type': 'http', 'host': tds[0], 'port':tds[1], 'address':tds[3]}
                results.append(r)
                r = {'type': 'https', 'host': tds[0], 'port':tds[1], 'address':tds[3]}
                results.append(r)
        return results


if __name__ == '__main__':

    seofangfa = SeoFangFa()
    r = seofangfa.get_proxys()
    print(r)
