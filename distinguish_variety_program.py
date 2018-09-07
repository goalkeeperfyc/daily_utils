# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 15:46:40 2018

@author: fangyucheng
"""


import copy
import datetime
import pandas as pd
from crawler_sys.utils import Metaorphosis as meta
from timeShiftAggregation.convert_csm_time_to_ISO import convert_csm_time_to_ISO
from timeShiftAggregation.trans_strtime_to_second import strtime_to_second


def variety_program(csvname, output_path):
    data_lst = meta.csv_to_lst_whth_headline(csvname)

    #删除无关数据
    count = 0
    for line in data_lst:
        if line['name'] == 'Start of Transmission' or line['name'] == 'End of Transmission':
            data_lst.remove(line)
            count += 1
            if count == 500:
                print('remove 500 data')
                count = 0

    #周几的变化
    weekday_dic = {'周日': 0,
                   '周一': 1,
                   '周二': 2,
                   '周三': 3,
                   '周四': 4,
                   '周五': 5,
                   '周六': 6}

    #加ID
    count = 1
    for line in data_lst:
        line['id'] = count
        count += 1

    try:
        data_lst[0]['dura']
        test_dura = 1
    except:
        test_dura = 0
        print("duration exists")
    #转化指标
    for line in data_lst:
        line['start'] = convert_csm_time_to_ISO(line['date'] + ' ' + line['start_time'])
        line['end'] = convert_csm_time_to_ISO(line['date'] + ' ' + line['end_time'])
        line['rate'] = float(line['rate'])
        line['time_shift'] = float(line['time_shift'])
        line['start_hour'] = datetime.datetime.strptime(line['start'], '%Y-%m-%d %H:%M:%S').hour
        line['ID'] = line['channel'] + line['name']
        line['start_datetime'] = datetime.datetime.strptime(line['start'], '%Y-%m-%d %H:%M:%S')
        line['start_time'] = line['start'].split(' ')[1]
        line['start_time_datetime'] = datetime.datetime.strptime(line['start_time'], '%H:%M:%S')
        line['week_num'] = weekday_dic[line['week']]
        if test_dura == 1:
            line['duration'] = strtime_to_second(line['dura'])

    #确定要处理的节目数
    ID_lst = []
    for line in data_lst:
        if line['ID'] not in ID_lst:
            ID_lst.append(line['ID'])

    #一个一个处理
    variety_distinguish = []
    for id_name in ID_lst:
        process_lst = []
        for line in data_lst:
            if line['ID'] == id_name:
                process_lst.append(line)

        if len(process_lst) == 1:
            for line in process_lst:
                line['ps'] = 1
                result_lst = copy.deepcopy(process_lst)
                meta.lst_to_csv(result_lst, output_path + '/norepeat' + id_name+'.csv')
                D0 = {'name':id_name, 'cate':'only one time'}
                variety_distinguish.append(D0)
            continue

    #判断有无重播
        date_lst = []
        for line in process_lst:
            date = line['date']
            if date not in date_lst:
                date_lst.append(date)
    #相邻的两个日期差值相近
        if len(date_lst) == len(process_lst) and len(date_lst) >= 5:
            start_time_lst = []
            for line in process_lst:
                start_time_lst.append(line['start_time_datetime'])
                start_time_range = max(start_time_lst) - min(start_time_lst)
            if start_time_range <= datetime.timedelta(0, 7200):
                line['ps'] = 1
                result_lst = copy.deepcopy(process_lst)
                meta.lst_to_csv(result_lst, output_path + '/dailypublish' + id_name + '.csv')
                D0 = {'name':id_name, 'cate':'daily'}
                variety_distinguish.append(D0)
                continue

#        df_process = pd.DataFrame(process_lst)
#        mean = df_process['rate'].mean()
        for line in process_lst:
            if line['start_hour'] >= 11 and line['start_hour'] <= 13:
                line['ps'] = 1
            else:
                line['ps'] = 0
    #将两个都是1的放入first_lst

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
            meta.lst_to_csv(result_lst, output_path + '/onlyonefirst' + id_name + '.csv')
            D0 = {'name':id_name, 'cate':'first only one'}
            variety_distinguish.append(D0)
        else:
            meta.lst_to_csv(result_lst, output_path + '/' + id_name + '.csv')
            D0 = {'name':id_name, 'cate':'normal'}
            variety_distinguish.append(D0)

if __name__ == '__main__':
    variety_program(csvname='F:/time_shift/test_data/document/walk_into_science.csv', 
                    output_path='F:/time_shift/test_data/document')
    
