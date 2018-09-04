# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 18:02:58 2018

@author: fangyucheng
"""

import datetime
from crawler_sys.utils import Metaorphosis as meta

first_published_program_lst = []
daily_program_lst = meta.csv_to_lst_whth_headline('F:/time_shift/test_data/variety/湖南卫视声临其境.csv')

for line in daily_program_lst:
    try:
        line['parent_id'] = str(int(float(line['parent_id'])))
    except:
        pass

def accumulate_daily_time_shift(first_published_program_lst, daily_program_lst):
    #将daily data 的首播信息放入首播节目列表
    for line in daily_program_lst:
        if line['ps'] == '1':
            line['time_shift_sum'] = 0
            first_published_program_lst.append(line)

    for repeat_program in daily_program_lst:
        for first_published in first_published_program_lst:
            if repeat_program['parent_id'] == first_published['id']:
                first_published['time_shift_sum'] += (float(repeat_program['time_shift']) * 
                                                      float(repeat_program['duration']) / 
                                                      float(first_published['duration']))
                print(first_published['time_shift_sum'])
                first_published['updata_time'] = str(datetime.datetime.now())[:19]

    for first_published in first_published_program_lst:
        first_published['time_shift_result'] = (float(first_published['time_shift_sum']) +
                                                float(first_published['time_shift']))

    return first_published_program_lst

if __name__ == '__main__':
    test_data = accumulate_daily_time_shift(first_published_program_lst, daily_program_lst)
    
