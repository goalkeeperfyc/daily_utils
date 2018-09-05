# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 15:49:20 2018

@author: fangyucheng
"""

import pymysql

host = '192.168.100.11'
user_name = 'fangyucheng'
password = 'csm@1234'

connection = pymysql.connect(host=host,
                             user=user_name,
                             password=password,
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)