# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 10:49:24 2018

@author: fangyucheng
"""


def strtime_to_second(strtime):
    strtime_lst = strtime.split(':')
    if len(strtime_lst) == 2:
        second = int(strtime_lst[0])*60 + int(strtime_lst[1])
        return second
    if len(strtime_lst) == 3:
        second = int(strtime_lst[0])*3600 + int(strtime_lst[1])*60 + int(strtime_lst[2])
        return second