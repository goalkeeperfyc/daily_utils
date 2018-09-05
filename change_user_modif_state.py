# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 14:20:26 2018

@author: zhouyujiang
"""

#用户修改首播信息后，自动更新user_modif_state表
from mysql_tool import func_mysql_update_line_by_line
def change_user_modif_state_start(db):
    tablename = 'user_modif_state'
    update_dict = {"state":1}
    key_dict = {"id":1}
    func_mysql_update_line_by_line(db, tablename, update_dict, key_dict)
def change_user_modif_state_end(db):
    tablename = 'user_modif_state'
    update_dict = {"state":0}
    key_dict = {"id":1}
    func_mysql_update_line_by_line(db, tablename, update_dict, key_dict)