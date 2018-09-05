# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 17:13:22 2018

@author: zhouyujiang
"""

#查找数据写入到mysql中
import pymysql
from mysql_tool import func_write_into_mysql_with_unique
all_dict_list = []
with open(r'D:\py_code_time_shift\time_shift\happy_camp.csv', 'r')as f:
    head = f.readline()
    head_list = head.strip().split(',')
    for i in f:
        line = i.strip().split(',')
        line_dict = dict(zip(head_list,line))
        all_dict_list.append(line_dict)

first_play_info_list = []


for one_dict in all_dict_list:
    first_play_info_dict = {}
    if int(one_dict['parent']) != 0:
            first_play_info_dict['first_play_program_id'] = one_dict['parent']
            first_play_info_dict['time_shift_id'] = one_dict['ID']
            first_play_info_list.append(first_play_info_dict)
host = '192.168.100.11'
user = 'root'
password = 'csm@1234'
databsase = 'bdd_time_shift'
tablename = 'time_shift_information'
log_file = open('test_log', 'w')

func_write_into_mysql_with_unique(host, user, password, databsase, tablename, log_file, data_dict_list=first_play_info_list)
            
        
        
log_file.close()
