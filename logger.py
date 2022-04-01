# -*- coding: utf-8 -*-
# @Author  : LG

import logging
from logging.handlers import RotatingFileHandler


def Logger(save_path='proxy.log', debug:bool=False):
    level = logging.DEBUG if debug else logging.INFO
    logger = logging.Logger('')
    formatter = logging.Formatter('%(asctime)s - %(thread)d - %(threadName)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(save_path, maxBytes=1024*1024*1, backupCount=5)  # 5M
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
