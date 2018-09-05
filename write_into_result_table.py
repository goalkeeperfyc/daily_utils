# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 17:53:50 2018

@author: zhouyujiang
"""
from mysql_tool import func_search_from_mysql_date
from mysql_tool import func_search_from_mysql_equal
#from 
#调用函数写入结果表
#这个函数应该只需要更新结果表
#第一步筛选近1个月首播数据，从time_shift_info表中取出
#一：找出某个时间段里所有的首播以及它的重播信息,这里先找到全量的数据不限制时间。


host = '192.168.100.11'
user = 'root'
password = 'csm@1234'
database = 'bdd_time_shift'
tablename = 'time_shift_information'
log_file = open('test_log', 'w')
#start_time = ''#这里不限制开始和结束时间，因为测试阶段数据不足，
#end_time = ''  #程序会选择所有时间短的数据
date_source = 'create_time'#这里选择创建时间，以后每天都按照创建时间提取数据
#need_dict =[]             
datetime_dict = func_search_from_mysql_date(host, user, password,
                                            database, tablename,
                                            log_file, date_source)
#找到首播数据对应的重播数据
#first_set = set() 
#replay_set = set()
one_first_dict ={}
for one_first in datetime_dict:
    first_program_id = one_first['first_play_program_id']
    replay_program_id = one_first['time_shift_id']
    if first_program_id in one_first_dict:
        one_first_dict[first_program_id].append(replay_program_id)
    else:
        one_first_dict[first_program_id] = []
        one_first_dict[first_program_id].append(replay_program_id)
tablename = 'all_program_information' 
for line_dict in one_first_dict:
    data_dict_list = [{'program_id':line_dict}]
    first_play_info = func_search_from_mysql_equal(host, user, password, database,
                                                   tablename,log_file,
                                                   data_dict_list=data_dict_list)
    
    
        
