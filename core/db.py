# -*- coding: utf-8 -*-
# @Author  : LG

import sqlite3
from queue import Queue


class DataBase:
    _path = None
    _queue = Queue(maxsize=1)

    def __init__(self, path, logger=None):
        self._path = path
        self.logger = logger

        self._init_db()
        self._create_conn()

    def _init_db(self):
        conn = sqlite3.connect(self._path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS proxys(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        host TEXT NOT NULL,
        port TEXT NOT NULL,
        anonymity TEXT NOT NULL,
        address TEXT,
        checktime TEXT)""")
        cursor.close()
        conn.close()
        if self.logger is not None:
            self.logger.info('Init database, create table proxys.')

    def _create_conn(self):
        conn = sqlite3.connect(self._path, check_same_thread=False)
        self._queue.put(conn)

    def _close(self, conn, cursor):
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        self._create_conn()

    def insert(self, type, host, port, anonymity, address='', checktime=''):
        conn = self._queue.get()
        cursor = conn.cursor()
        sql = 'INSERT INTO proxys (type, host, port, anonymity, address, checktime) VALUES (?, ?, ?, ?, ?, ?);'
        try:
            cursor.execute(sql, (type, host, port, anonymity, address, checktime))
            conn.commit()
            if self.logger is not None:
                self.logger.debug('Insert new proxy. {}://{}:{}'.format(type, host, port))
        except Exception as e:
            conn.rollback()
            if self.logger is not None:
                self.logger.warning('Insert failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        return True

    def get_one(self, type:str = None, anonymity:str = None):
        conn = self._queue.get()
        cursor = conn.cursor()
        if type is None and anonymity is None:
            sql = "select * from proxys order by random() limit 1;"
        else:
            if type is not None and anonymity is not None:
                sql = "select * from proxys where (type='{}' and anonymity='{}') order by random() limit 1;".format(type, anonymity)
            elif type is not None:
                sql = "select * from proxys where type='{}' order by random() limit 1;".format(type)
            else:
                sql = "select * from proxys where anonymity='{}' order by random() limit 1;".format(anonymity)

        results = []
        try:
            results = cursor.execute(sql).fetchall()
            if len(results)>0:
                results = [{'id' : r[0], 'type' : r[1], 'host':r[2] , 'port': r[3],
                            'anonymity':r[4], 'address' : r[5], 'checktime': r[6]} for r in results]
        except Exception as e:
            if self.logger is not None:
                self.logger.warning('Select failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        return results

    def get_all(self):
        conn = self._queue.get()
        cursor = conn.cursor()
        sql = 'SELECT * FROM proxys;'
        results = []
        try:
            results = cursor.execute(sql).fetchall()
            if len(results)>0:
                results = [{'id': r[0], 'type': r[1], 'host':r[2], 'port': r[3],
                            'anonymity':r[4], 'address': r[5], 'checktime': r[6]} for r in results]
        except Exception as e:
            if self.logger is not None:
                self.logger.warning('Select failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        return results

    def is_exist_proxy(self, type, host, port):
        conn = self._queue.get()
        cursor = conn.cursor()
        sql = "select * from proxys where (type='{}' and host='{}' and port='{}');".format(type, host, port)
        results = []
        try:
            results = cursor.execute(sql).fetchall()
            if len(results)>0:
                results = [{'id' : r[0], 'type' : r[1], 'host':r[2] ,
                            'port': r[3], 'anonymity':r[4], 'address' : r[5]} for r in results]
        except Exception as e:
            if self.logger is not None:
                self.logger.warning('Select failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        if len(results) > 0:
            return True
        else:
            return False

    def delete_by_id(self, id):
        conn = self._queue.get()
        cursor = conn.cursor()
        sql = "DELETE FROM proxys WHERE id={}".format(id)
        try:
            cursor.execute(sql)
            conn.commit()
            if self.logger is not None:
                self.logger.debug('Delete invalid proxy. The id is {}.'.format(id))
        except Exception as e:
            conn.rollback()
            if self.logger is not None:
                self.logger.warning('Delete failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        return True

    def update_anonymity_by_id(self, anonymity:str, id:int):
        conn = self._queue.get()
        cursor = conn.cursor()
        sql = "UPDATE proxys SET anonymity='{}' WHERE id={}".format(anonymity, id)
        try:
            cursor.execute(sql)
            conn.commit()
            if self.logger is not None:
                self.logger.debug('Update proxy with id {}. Anonymity is {}.'.format(id, anonymity))
        except Exception as e:
            conn.rollback()
            if self.logger is not None:
                self.logger.warning('Update failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        return True

    def update_checktime_by_id(self, checktime:str, id:int):
        conn = self._queue.get()
        cursor = conn.cursor()
        sql = "UPDATE proxys SET checktime='{}' WHERE id={}".format(checktime, id)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            if self.logger is not None:
                self.logger.warning('Update failed! {}'.format(e))
        finally:
            self._close(conn, cursor)
        return True


if __name__ == '__main__':
    from threading import Thread
    import random
    db = DataBase('test.db')
    # t1 = Thread(target=db.insert, args=("http2", '192.0.110.1', '8090', '111'))
    # t2 = Thread(target=db.get_one, args=(None, '33',))
    # print(r)
    # t1.start()
    # t2.start()

    # for _ in range(10):
    #     db.insert('{}'.format(random.choice(['http', 'https'])),
    #               '192.0.110.{}'.format(random.randint(0, 100)),
    #               '{}'.format(random.randint(0, 10000)),
    #               random.choice(['a', 'h', 't', 'uk']))

    # rs = db.get_all()
    # for r in rs:
    #     print(r)

    # db.update_anonymity_by_id('t', 3)

    # print(db.get_one())