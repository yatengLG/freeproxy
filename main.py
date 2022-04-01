# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask, request, render_template
from core import Engine
from configs import db_path, logger_path
from logger import Logger
from json import dumps


app = Flask(__name__)


@app.route('/get_proxy', methods=['POST'])
def get_proxy():
    type = request.form.get('type')
    anonymity = request.form.get('anonymity')
    r = engine.get_proxy(type, anonymity)
    r = dumps(r)
    return r


@app.route('/get_all_proxy', methods=['GET'])
def get_all_proxy():
    rs = engine.database.get_all()
    rs = {'num': len(rs), 'proxys': rs}
    rs = dumps(rs)
    return rs


@app.route('/proxys')
def hello():
    rs = engine.database.get_all()
    num = len(rs)
    return render_template('proxys.html', num=num, proxys=rs)


if __name__ == '__main__':
    from threading import Thread

    logger = Logger(logger_path)

    engine = Engine(db_path, logger)
    engine.auto_crawl_timesleep = 120
    engine.auto_check_timesleep = 60
    engine.register_default()

    t = Thread(target=engine.run, name='engine')
    t.start()

    app.run(host='127.0.0.1', port=5000)
    t.join()

