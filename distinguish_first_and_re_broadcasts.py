# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 18:59:40 2018

@author: fangyucheng
"""


import copy
import datetime
import pandas as pd
from crawler_sys.utils import Metaorphosis as meta
from crawler_sys.utils.output_log import output_log
from timeShiftAggregation.convert_csm_time_to_ISO import convert_csm_time_to_ISO

#打印日志
write_log_into_txt = output_log('time_shift', 'variety')

#从头开始
data_lst = meta.csv_to_lst_whth_headline('F:/time_shift/sample_data_2018_52_city.csv')

#删除无关数据
count = 0
for line in data_lst:
    if line['name'] == 'Start of Transmission' or line['name'] == 'End of Transmission':
        data_lst.remove(line)
        count += 1
        if count == 500:
            print('remove 500 data')
            count = 0

#转换一下周几的表达
weekday_dic = {'周日': 0,
               '周一': 1,
               '周二': 2,
               '周三': 3,
               '周四': 4,
               '周五': 5,
               '周六': 6}
for line in data_lst:
    line['week_num'] = weekday_dic[line['week']]

#加ID
count = 0
for line in data_lst:
    line['id'] = count
    count += 1
    
#写入文件
meta.dic_lst_to_file(data_lst, 'F:/time_shift/sample_data_2018_52_city_cleaned')

#以后从这里开始
data_lst = meta.dic_file_to_lst('F:/time_shift/sample_data_2018_52_city_cleaned')

#转化指标
for line in data_lst:
    line['start'] = convert_csm_time_to_ISO(line['date'] + ' ' + line['start_time'])
    line['end'] = convert_csm_time_to_ISO(line['date'] + ' ' + line['end_time'])
    line['rate'] = float(line['rate'])
    line['time_shift'] = float(line['time_shift'])
    line['start_hour'] = datetime.datetime.strptime(line['start'],  '%Y-%m-%d %H:%M:%S').hour
    line['ID'] = line['channel'] + line['name']
    line['start_datetime'] = datetime.datetime.strptime(line['start'], '%Y-%m-%d %H:%M:%S')
    line['start_time'] = line['start'].split(' ')[1]
    line['start_time_datetime'] = datetime.datetime.strptime(line['start_time'], '%H:%M:%S')


#处理电视剧
variety_lst = []
cate_name = '综艺'

for line in data_lst:
    if line['category'] == cate_name:
        variety_lst.append(line)


#找到所有综艺节目的名字
ID_lst = []
for line in variety_lst:
    if line['ID'] not in ID_lst:
        ID_lst.append(line['ID'])

#一个一个处理
variety_distinguish = []
for id_name in ID_lst:
    process_lst = []
    for line in variety_lst:
        if line['ID'] == id_name:
            process_lst.append(line)

    if len(process_lst) == 1:
        for line in process_lst:
            line['ps'] = 1
            result_lst = copy.deepcopy(process_lst)
            meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/norepeat'+id_name+'.csv')
            write_log_into_txt.info('%s publish only one time' % id_name)
            D0 = {'name':id_name,'cate':'only one time'}
            variety_distinguish.append(D0)
        continue

#判断有无重播
    date_lst = []
    for line in process_lst:
        date = line['date']
        if date not in date_lst:
            date_lst.append(date)
#相邻的两个日期差值相近
    if len(date_lst) == len(process_lst) and len(date_lst) >=5:
        start_time_lst = []
        for line in process_lst:
            start_time_lst.append(line['start_time_datetime'])
            start_time_range = max(start_time_lst) - min(start_time_lst)
        if start_time_range <= datetime.timedelta(0, 7200):
            line['ps'] = 1
            result_lst = copy.deepcopy(process_lst)
            meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/dailypublish'+id_name+'.csv')
            write_log_into_txt.info('%s is dailypublished' % id_name)
            D0 = {'name':id_name,'cate':'daily'}
            variety_distinguish.append(D0)
            continue

    df_process = pd.DataFrame(process_lst)
    mean = df_process['rate'].mean()
    for line in process_lst:
        if line['rate'] > mean:
            line['ps1'] = 1
            line['ps1_poss'] = (line['rate'] - mean)/mean
        else:
            line['ps1'] = 0
            line['ps1_poss'] = 0
        if line['start_hour'] >= 19 and line['start_hour'] <=22:
            line['ps2'] = 1
        else:
            line['ps2'] = 0
#将两个都是1的放入first_lst

    for line in process_lst:
        if line['ps1'] == 1 and line['ps2'] == 1:
            line['ps'] = 1
        else:
            line['ps'] = 0

#保证一天只有一个首播
    date_lst = []
    first_lst = []
    for line in process_lst:
        if line['ps'] == 1:
            if line['date'] not in date_lst:
                date_lst.append(line['date'])
                first_lst.append(line)
            else:
                for line2 in first_lst:
                    if line2['date'] == line['date']:
                        if line2['rate'] > line['rate']:
                            line['ps'] = 0
                        else:
                            line2['ps'] = 0
    re_publish = []
    first_publish = []
    for line in process_lst:
        if line['ps'] == 0:
            re_publish.append(line)
        else:
            first_publish.append(line)
    if first_publish == []:
        write_log_into_txt.info('%s program publish on daily' %id_name)
        continue
#重播找首播
    result_lst = []
    for line in re_publish:
        time_span = datetime.timedelta(50)
        for first in first_publish:
            difference = line['start_datetime'] - first['start_datetime']
            if difference > datetime.timedelta(0) and difference < time_span:
                time_span = difference
                line['parent_id'] = first['id']
        result_lst.append(line)
    for line in first_publish:
        result_lst.append(line)
    if len(first_publish) == 1:
        meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/onlyonefirst'+id_name+'.csv')
        write_log_into_txt.info('%s is only one first published' % id_name)
        D0 = {'name':id_name,'cate':'first only one'}
        variety_distinguish.append(D0)
    else:
        meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/'+id_name+'.csv')
        write_log_into_txt.info('%s is normal program' % id_name)
        D0 = {'name':id_name,'cate':'normal'}
        variety_distinguish.append(D0)

#从综艺节目开始
variety_lst = []
cate_name = '综艺'

for line in data_lst:
    if line['category'] == cate_name:
        variety_lst.append(line)


#找到所有综艺节目的名字
ID_lst = []
for line in variety_lst:
    if line['ID'] not in ID_lst:
        ID_lst.append(line['ID'])

#一个一个处理
variety_distinguish = []
for id_name in ID_lst:
    process_lst = []
    for line in variety_lst:
        if line['ID'] == id_name:
            process_lst.append(line)

    if len(process_lst) == 1:
        for line in process_lst:
            line['ps'] = 1
            result_lst = copy.deepcopy(process_lst)
            meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/norepeat'+id_name+'.csv')
            write_log_into_txt.info('%s publish only one time' % id_name)
            D0 = {'name':id_name,'cate':'only one time'}
            variety_distinguish.append(D0)
        continue

#判断有无重播
    date_lst = []
    for line in process_lst:
        date = line['date']
        if date not in date_lst:
            date_lst.append(date)
#相邻的两个日期差值相近
    if len(date_lst) == len(process_lst) and len(date_lst) >=5:
        start_time_lst = []
        for line in process_lst:
            start_time_lst.append(line['start_time_datetime'])
            start_time_range = max(start_time_lst) - min(start_time_lst)
        if start_time_range <= datetime.timedelta(0, 7200):
            line['ps'] = 1
            result_lst = copy.deepcopy(process_lst)
            meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/dailypublish'+id_name+'.csv')
            write_log_into_txt.info('%s is dailypublished' % id_name)
            D0 = {'name':id_name,'cate':'daily'}
            variety_distinguish.append(D0)
            continue

    df_process = pd.DataFrame(process_lst)
    mean = df_process['rate'].mean()
    for line in process_lst:
        if line['rate'] > mean:
            line['ps1'] = 1
            line['ps1_poss'] = (line['rate'] - mean)/mean
        else:
            line['ps1'] = 0
            line['ps1_poss'] = 0
        if line['start_hour'] >= 19 and line['start_hour'] <=22:
            line['ps2'] = 1
        else:
            line['ps2'] = 0
#将两个都是1的放入first_lst

    for line in process_lst:
        if line['ps1'] == 1 and line['ps2'] == 1:
            line['ps'] = 1
        else:
            line['ps'] = 0

#保证一天只有一个首播
    date_lst = []
    first_lst = []
    for line in process_lst:
        if line['ps'] == 1:
            if line['date'] not in date_lst:
                date_lst.append(line['date'])
                first_lst.append(line)
            else:
                for line2 in first_lst:
                    if line2['date'] == line['date']:
                        if line2['rate'] > line['rate']:
                            line['ps'] = 0
                        else:
                            line2['ps'] = 0
    re_publish = []
    first_publish = []
    for line in process_lst:
        if line['ps'] == 0:
            re_publish.append(line)
        else:
            first_publish.append(line)
    if first_publish == []:
        write_log_into_txt.info('%s program publish on daily' %id_name)
        continue
#重播找首播
    result_lst = []
    for line in re_publish:
        time_span = datetime.timedelta(50)
        for first in first_publish:
            difference = line['start_datetime'] - first['start_datetime']
            if difference > datetime.timedelta(0) and difference < time_span:
                time_span = difference
                line['parent_id'] = first['id']
        result_lst.append(line)
    for line in first_publish:
        result_lst.append(line)
    for line in result_lst:
        if line['ps'] == 1:
            line['parent_id'] = 0
    if len(first_publish) == 1:
        meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/onlyonefirst'+id_name+'.csv')
        write_log_into_txt.info('%s is only one first published' % id_name)
        D0 = {'name':id_name,'cate':'first only one'}
        variety_distinguish.append(D0)
    else:
        meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/'+id_name+'.csv')
        write_log_into_txt.info('%s is normal program' % id_name)
        D0 = {'name':id_name,'cate':'normal'}
        variety_distinguish.append(D0)
