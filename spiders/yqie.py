# -*- coding: utf-8 -*-
# @Author  : LG


from core.spider import SpiderBC
import requests
from bs4 import BeautifulSoup


class YQie(SpiderBC):
    def __init__(self):
        super(YQie, self).__init__()
        self.base_url = 'http://ip.yqie.com/ipproxy.htm'

    def get_proxys(self):
        results = []
        response = requests.get(self.base_url, headers=self.headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find('table', {'id':'GridViewOrder'})
            trs = table.find_all('tr')[1:]
            for tr in trs:
                tds = tr.find_all('td')
                tds = [td.text for td in tds]
                r = {'type':tds[4].lower(), 'host': tds[0], 'port':tds[1], 'address':tds[2]}
                if tds[3] == '高匿':
                    r['anonymity'] = 'h'
                elif tds[3] == '匿名':
                    r['anonymity'] = 'a'
                elif tds[3] == '普通':
                    r['anonymity'] = 't'
                else:
                    r['anonymity'] = ''
                results.append(r)
        return results


if __name__ == '__main__':
    YQ = YQie()
    proxys = YQ.get_proxys()
    print(proxys)