# -*- coding:utf-8 -*-
'''
Created on 2011/12/28
Gunicorn定義ファイル

@author: shinyorke
'''

bind = 'unix:/var/run/gunicorn/gunicorn.sock'
workers = 3
# workerはデフォルトのやつを使う
#worker_class = 'egg:meinheld#gunicorn_worker'
pidfile = '/var/run/gunicorn/gunicorn.pid'
