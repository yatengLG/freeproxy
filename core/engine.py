# -*- coding: utf-8 -*-
# @Author  : LG

from .db import DataBase
from .checker import Checker
from .spider import SpiderBC
from threading import Timer, Thread
import time
from datetime import datetime


class Engine:
    def __init__(self, db_path, logger=None):
        self.logger = logger

        self.checker = Checker(self.logger)
        self.database = DataBase(db_path, self.logger)
        self.spiders = {}
        self.auto_crawl_timesleep = 180
        self.auto_check_timesleep = 60

    def register_spider(self, name:str, spider:SpiderBC):
        if name not in self.spiders:
            self.spiders[name] = spider

    def register_default(self):
        from spiders import FateZero, YQie, SeoFangFa, PubProxy, ProxyLists, AB57, Ip3366
        self.register_spider(FateZero.__name__, FateZero())
        self.register_spider(SeoFangFa.__name__, SeoFangFa())
        self.register_spider(PubProxy.__name__, PubProxy())
        self.register_spider(AB57.__name__, AB57())
        self.register_spider(Ip3366.__name__, Ip3366())
        # 以下代理有效ip较少，但耗时较长
        # self.register_spider(YQie.__name__, YQie())
        # self.register_spider(ProxyLists.__name__, ProxyLists())

    def crwal_proxys(self):
        if self.logger is not None:
            self.logger.info("Start crwal.")

        for name, spider in self.spiders.items():
            n_new = 0
            n_exist = 0
            proxys = spider.get_proxys()
            time1 = time.time()
            for proxy in proxys:
                type = proxy.get('type', '')
                host = proxy.get('host', '')
                port = proxy.get('port', '')
                anonymity = proxy.get('anonymity', '')
                address = proxy.get('address', '')
                r = self.checker.check(type, host, port)
                if r:
                    if self.database.is_exist_proxy(type, host, port):
                        n_exist += 1
                    else:
                        self.database.insert(type, host, port, r['anonymity'], address, datetime.strftime(datetime.now(), "%m-%d %H:%M:%S"))
                        n_new += 1
            if self.logger is not None:
                self.logger.info("┌{}┐".format('-'*58))
                self.logger.info("| {:^15s} | {:^5s} | {:^5s} | {:^5s} | {:^4s} | {:^7s} |".format('spider', 'new', 'exist', 'total', 'rate', 'cost'))
                self.logger.info("|{}|{}|{}|{}|{}|{}|".format('-'*17, '-'*7, '-'*7, '-'*7, '-'*6, '-'*9))
                self.logger.info("| {:^15s} | {:^5d} | {:^5d} | {:^5d} | {:.2f} | {:^7.2f} |".format(name, n_new, n_exist, len(proxys), (n_new+n_exist)/len(proxys), time.time()-time1))
                self.logger.info("└{}┘".format('-'*58))

        if self.logger is not None:
            self.logger.info("End crwal.")

    def auto_crawl(self):
        self.crwal_proxys()
        t = Timer(self.auto_crawl_timesleep, self.auto_crawl)
        t.setName('auto crawl')
        t.start()

    def check_db(self):
        if self.logger is not None:
            self.logger.info("Start check.")
        n = 0
        time1 = time.time()
        results = self.database.get_all()
        for result in results:
            id = result['id']
            type = result['type']
            host = result['host']
            port = result['port']
            anonymity = result['anonymity']
            r = self.checker.check(type, host, port)
            if not r:
                self.database.delete_by_id(id)
                n += 1
            else:
                if r['anonymity'] != anonymity:
                    self.database.update_anonymity_by_id(r['anonymity'], id)
                self.database.update_checktime_by_id(datetime.strftime(datetime.now(), "%m-%d %H:%M:%S"), id)
        if self.logger is not None:
            self.logger.info("┌{}┐".format('-'*39))
            self.logger.info("| {:^7s} | {:^7s} | {:^7s} | {:^7s} |".format("valid", "invalid", "total", "cost/s"))
            self.logger.info("| {:^7d} | {:^7d} | {:^7d} | {:^7.2f} |".format(len(results)-n, n, len(results), time.time()-time1))
            self.logger.info("└{}┘".format('-'*39))
            self.logger.info("End check.")

    def auto_check(self):
        self.check_db()
        t = Timer(self.auto_check_timesleep, self.auto_check)
        t.setName('auto check')
        t.start()

    def get_proxy(self, type:str=None, anonymity:str=None):
        proxy = self.database.get_one(type, anonymity)
        return proxy

    def run(self):
        if len(self.spiders) < 1:
            if self.logger is not None:
                self.logger.error("The number of spiders is zero!")
            raise AttributeError("The number of spiders is zero! Please register the spider before running.")

        thread1 = Thread(target=self.auto_crawl, name='auto crawl')
        thread2 = Thread(target=self.auto_check, name='auto check')
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

