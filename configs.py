# -*- coding: utf-8 -*-
# @Author  : LG

import os
save_dir = 'save_dir'
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

db_path = os.path.join(save_dir, 'proxy.db')
logger_path = os.path.join(save_dir, 'proxy.log')
