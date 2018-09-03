# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 17:03:59 2018

@author: Hanye
"""

import re
import datetime

def convert_csm_time_to_ISO(csm_datetime_str):
    # '2018-05-17 25:56:00'
    csm_datetime_str = csm_datetime_str.replace('/', '-')
    find_time_str_raw = re.findall('\s[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}', csm_datetime_str)
    if find_time_str_raw != []:
        time_str_split = find_time_str_raw[0].split(':')
        hour_str = time_str_split[0][1:]
        hour_int = int(hour_str)
        if hour_int >= 24:
            find_date_str_raw = re.findall('\d+-\d+-\d+', csm_datetime_str)
            if find_date_str_raw != []:
                date_T = datetime.datetime.strptime(find_date_str_raw[0], '%Y-%m-%d')
                date_T_c = date_T + datetime.timedelta(days=1)
                date_str_c = date_T_c.isoformat()[:10]
                hour_int_c = hour_int - 24
                time_str_split[0] = str(hour_int_c)
                time_str_c = ':'.join(time_str_split)
                datetime_str_c = date_str_c + ' ' + time_str_c
                return datetime_str_c
            else:
                return None
        else:
            return csm_datetime_str
    else:
        return None
