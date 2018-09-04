# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 16:39:45 2018

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

drama_lst = []
cate_name = '电视剧'

for line in data_lst:
    if line['category'] == cate_name:
        drama_lst.append(line)

process_lst = []
for line in data_lst:
    if line['name'] == '温暖的弦':
       process_lst.append(line)

id_name = '温暖的弦'
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
    if line['ps2'] == 1:
        line['ps'] = 1
    else:
        line['ps'] = 0

re_publish = []
first_publish = []
for line in process_lst:
    if line['ps'] == 0:
        re_publish.append(line)
    else:
        first_publish.append(line)
if first_publish == []:
    write_log_into_txt.info('%s program publish on daily' %id_name)

#重播找首播
result_lst = []
for line in re_publish:
    print(line['ps'])
    time_span = datetime.timedelta(50)
    count = 0
    for first in first_publish:
        try:
            first['parent_id']
            print(count)
            return line
        except:
            pass
        count+=1
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

else:
    meta.lst_to_csv(result_lst, 'F:/time_shift/test_data/variety/'+id_name+'.csv')
    write_log_into_txt.info('%s is normal program' % id_name)
    D0 = {'name':id_name,'cate':'normal'}





