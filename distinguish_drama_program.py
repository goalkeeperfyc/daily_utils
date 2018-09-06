# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 16:39:45 2018

@author: fangyucheng
"""

#import copy
import datetime
#import pandas as pd
from crawler_sys.utils import Metaorphosis as meta
from crawler_sys.utils.output_log import output_log
from timeShiftAggregation.convert_csm_time_to_ISO import convert_csm_time_to_ISO
from timeShiftAggregation.trans_strtime_to_second import strtime_to_second

#打印日志
write_log_into_txt = output_log('time_shift', 'variety')

def drama_program(csvname, output_path):
    data_lst = meta.csv_to_lst_whth_headline(csvname)

    #加id
    count = 1
    for line in data_lst:
        line['id'] = count
        count += 1

    #将strtime转化为second
    try:
        data_lst[0]['dura']
        test_dura = 1
    except:
        test_dura = 0
        print("duration exists")

    #周几的变化
    weekday_dic = {'周日': 0,
                   '周一': 1,
                   '周二': 2,
                   '周三': 3,
                   '周四': 4,
                   '周五': 5,
                   '周六': 6}

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
        line['week_num'] = weekday_dic[line['week']]
        if test_dura == 1:
            line['duration'] = strtime_to_second(line['dura'])

    #挑出所有要处理的节目
    ID_lst = []
    for line in data_lst:
        if line['ID'] not in ID_lst:
            ID_lst.append(line['ID'])

    #一个一个安排
    for id_name in ID_lst:
        process_lst = []
        for line in data_lst:
            if line['ID'] == id_name:
                process_lst.append(line)

        #黄金时间播出的定为首播
        for line in process_lst:
            if line['start_hour'] >= 19 and line['start_hour'] <=22:
                line['ps'] = 1
            else:
                line['ps'] = 0
        #计算平均值
        #df_process = pd.DataFrame(process_lst)
        #mean = df_process['rate'].mean()
        re_publish = []
        first_publish = []
        for line in process_lst:
            if line['ps'] == 0:
                re_publish.append(line)
            else:
                first_publish.append(line)
        if first_publish == []:
            print('%s program publish on daily' %id_name)
        result_lst = []
        #判断是否有集数信息
        video_num = process_lst[0]['集数']
        if video_num == '':
            for line in re_publish:
                time_span = datetime.timedelta(50)
                for first in first_publish:
                    difference = line['start_datetime'] - first['start_datetime']
                    if difference > datetime.timedelta(0) and difference < time_span:
                        time_span = difference
                        line['parent_id'] = first['id']
                result_lst.append(line)
        else:
            for line in re_publish:
                for first in first_publish:
                    if line['集数'] == first['集数']:
                        line['parent_id'] = first['id']
                result_lst.append(line)
        for line in first_publish:
            line['parent_id'] = 0
            result_lst.append(line)
    meta.lst_to_csv(result_lst, output_path + id_name + '.csv')

if __name__ == '__main__':
    test_drama = drama_program(csvname='F:/time_shift/test_data/drama/test_data.csv',
                               output_path='F:/time_shift/test_data/drama/')



