# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 18:02:58 2018

@author: fangyucheng
"""

import datetime

def accumulate_daily_time_shift(parent_dic, son_lst):
    try:
        parent_dic['time_shift_sum']
    except:
        parent_dic['time_shift_sum'] = 0
    for line in son_lst:
        parent_dic['time_shift_sum'] += (float(line['time_shift_rating']) * 
                                         float(line['duration']) / 
                                         float(parent_dic['duration']))
    parent_dic['updata_time'] = str(datetime.datetime.now())[:19]

    parent_dic['result_rating'] = (float(parent_dic['time_shift_sum']) +
                                   float(parent_dic['time_shift_rating']))

    return parent_dic

if __name__ == "__main__":
    parent_dic = {'program_id': 87,
                  'category': '综艺',
                  'program_name': '',
                  'channel': '湖南卫视',
                  'duration': 6057,
                  'live_rating': 0.9241,
                  'time_shift_rating': 0.1368,
                  'program_start': datetime.datetime(2018, 8, 18, 20, 18, 29),
                  'program_end': datetime.datetime(2018, 8, 18, 21, 59, 26),
                  'create_time': datetime.datetime(2018, 8, 31, 18, 21, 7),
                  'update_time': datetime.datetime(2018, 8, 31, 18, 21, 7),
                  'time_shift_sum': 0,
                  'updata_time': '2018-09-03 19:15:32',
                  'result_rating': 0.3145}
    son_lst = [{'program_id': 88,
                'category': '综艺',
                'program_name': '',
                'channel': '湖南卫视',
                'duration': 6615,
                'live_rating': 0.281,
                'time_shift_rating': 0.1777,
                'program_start': datetime.datetime(2018, 8, 19, 13, 35, 47),
                'program_end': datetime.datetime(2018, 8, 19, 15, 26, 2),
                'create_time': datetime.datetime(2018, 8, 31, 18, 21, 7),
                'update_time': datetime.datetime(2018, 8, 31, 18, 21, 7)}]
    t = accumulate_daily_time_shift(parent_dic, son_lst)