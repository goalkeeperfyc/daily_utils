# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 14:42:03 2018

@author: zhouyujiang
"""
#操作数据库工具。
#更新具有唯一索引的表，存在更新，不存在添加
#需要传数据库的ip,user、password、数据库名、表名、list[dict]
import pymysql

#def func_mysql_info_analyze(mysql_dict):
#    user = mysql_dict['user']
#    host = mysql_dict['host']
#    password = mysql_dict['password']


def func_write_into_mysql_with_unique(db, tablename, log_file, data_dict_list=[]):
    cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
    if len(data_dict_list) == 0:
        print('传入的数据为空',file=log_file)
        return None
    else:
        for one_modif_data in data_dict_list:
            if type(one_modif_data) != dict:
                print('传入的参数应该是字典{one_modif_data}'.format(one_modif_data=one_modif_data), file=log_file)
            else:
                replace_sql_first = 'REPLACE INTO {tablename}('.format(tablename=tablename)
                replace_sql_mind = ''
                replace_sql_end = ''
                for one_source in one_modif_data:
                    replace_sql_mind = replace_sql_mind+'{one_source},'.format(one_source=one_source)
                    replace_sql_end=replace_sql_end+'"{data}",'.format(data=one_modif_data[one_source])
                replace_sql_mind=replace_sql_mind[0:-1]
                replace_sql_mind=replace_sql_mind+') VALUES('
                replace_sql_end = replace_sql_end[0:-1]
                replace_sql_end = replace_sql_end+')'
                replace_sql=replace_sql_first+replace_sql_mind+replace_sql_end
                try:
                    cursor.execute(replace_sql)
                    db.commit()   
   
                except Exception as Argument:
                    print('错误已回滚：')
                    print(Argument)
                    db.rollback()
                
def func_search_from_mysql_equal(db, tablename,log_file, data_dict_list=[], need_dict=[]):
    cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
    if len(data_dict_list) == 0:
        print('传入的数据为空', file=log_file)
        return None
    else:
        for one_modif_data in data_dict_list:
            if type(one_modif_data) != dict:
                print('传入的参数应该是字典{one_modif_data}'.format(one_modif_data=one_modif_data), file=log_file)
            else:
                if need_dict == []:
                    select_sql_first = 'select * from {tablename} where '.format(tablename=tablename)
                else:
                    select_sql_first_first = 'select '
                    select_sql_first_mid = ''
                    select_sql_first_end = ' from {tablename} where '.format(tablename=tablename)
                    for  one in range(len(need_dict)):
                        if one != len(need_dict)-1:
                            select_sql_first_mid = select_sql_first_mid + need_dict[one] + ','
                        else:
                            select_sql_first_mid = select_sql_first_mid + need_dict[one]
                    select_sql_first =  select_sql_first_first + select_sql_first_mid + select_sql_first_end
                        
                select_sql_end = ''
                count = 0
                for one_source in one_modif_data:
                    count = count + 1
                    if count != len(one_modif_data):
                        select_sql_end = select_sql_end + '{one_source}={one_source_data} AND '.format(one_source, one_source_data=one_modif_data[one_source])
                    else:
                        select_sql_end = select_sql_end + '{one_source}={one_source_data}'.format(one_source, one_source_data=one_modif_data[one_source])
                    
                select_sql = select_sql_first + select_sql_end
                try:
                    cursor.execute(select_sql)
#                    db.commit()   
                    return cursor.fetchall()
                    
                except Exception as Argument:
                    print('错误：', file=log_file)
                    print(Argument, file=log_file)
#def func_write_into_mysql(host, user, password, database, tablename,log_file, data_dict_list=[]):
def func_search_from_mysql_date(db, tablename, log_file,date_source, start_time=None, end_time=None, need_dict=[]):
    cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
    if start_time is None and end_time is None:
        str_start_time = '2000-01-01'
        str_end_time = '2100-01-01'
    elif start_time is None and end_time is not None:
        str_start_time = '2000-01-01'
        str_end_time = end_time
    elif start_time is not  None and end_time is None:
        str_end_time = '2100-01-01'
        str_start_time = start_time
    else:
        str_end_time = end_time
        str_start_time =start_time
    if need_dict == []:
        select_date_sql = """select * from {tablename} where {date_source} between 
                        {str_start_time} and {str_end_time}""".format(tablename=tablename,
                        date_source=date_source, str_start_time=str_start_time,str_end_time=str_end_time)
    else:
        select_sql_first_first = 'select '
        select_sql_first_mid = ''
        select_sql_first_end = ' from {tablename} where '.format(tablename=tablename)
        for  one in range(len(need_dict)):
            if one != len(need_dict)-1:
                select_sql_first_mid = select_sql_first_mid + need_dict[one] + ','
            else:
                select_sql_first_mid = select_sql_first_mid + need_dict[one]
        select_sql_first =  select_sql_first_first + select_sql_first_mid + select_sql_first_end
        select_date_sql =select_sql_first + """{date_source} between 
                        {str_start_time} and {str_end_time}""".format(tablename=tablename,
                        date_source=date_source, str_start_time=str_start_time,str_end_time=str_end_time)
    try:
        cursor.execute(select_date_sql)
#        db.commit()   
        return cursor.fetchall()
    except Exception as Argument:
        print('错误：', file=log_file)
        print(Argument, file=log_file)
    

def func_mysql_update_line_by_line(db,tablename,date_source,update_dict, key_dict):
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    update_sql_first = 'UPDATE {tablename} SET '.format(tablename=tablename)
    update_sql_end = ''
    update_sql_mind = ''
    if type(update_dict) != dict:
        print('输入的update应该是个字典')
    else:
        update_dict_count = 0
        for one_update_dict in update_dict:
            update_dict_count = update_dict_count + 1
            if update_dict_count != len(update_dict):
                update_sql_mind = update_sql_mind + """{one_update_dict}={one_update_dict_source} ,
                 """.format(one_update_dict=one_update_dict, one_update_dict_source=update_dict[one_update_dict])
            else:
                update_sql_mind = update_sql_mind + """{one_update_dict}={one_update_dict_source}
                 """.format(one_update_dict=one_update_dict, one_update_dict_source=update_dict[one_update_dict])
    if type(key_dict) != dict:
        print('输入的key_dict应该是个字典')
    else:
        key_dict_count = 0
        for one_key in key_dict:
            key_dict_count = key_dict_count + 1
            if key_dict_count != len(key_dict):
                update_sql_end = """{one_key}={one_key_source} 
                                 AND """.format(one_key=one_key,
                                                one_key_source=key_dict[one_key])
            else:
                update_sql_end = """{one_key}={one_key_source} 
                                 """.format(one_key=one_key,
                                                one_key_source=key_dict[one_key])
        update_sql = update_sql_first + update_sql_mind + ' where ' + update_sql_end
        try:
            cursor.execute(update_sql)
            db.commit()   
        except Exception as Argument:
            print('错误已回滚：')
            db.rollback()

def func_select_some_in_list(db, tablename,in_key,in_list):
    cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
    
    in_sql = """select * from tablename where {in_key} in {in_list}""".format(in_key=in_key,
                                                                              in_list=in_list)

    try:
        cursor.execute(in_sql)
        return cursor.fetchall()
    
    except Exception as Argument:
        print('错误：')
        print(Argument)

    
                        

            
            
    
        
    
    
    
    


