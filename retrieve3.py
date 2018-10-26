#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import copy
import elasticsearch
import elasticsearch.helpers
import csv


reload(sys)
sys.setdefaultencoding('utf-8')
print (sys.getdefaultencoding())

hosts = '192.168.17.11'
port = 80
user_id = 'fangyucheng'
password = 'VK0FkWf1fV8f'
http_auth = (user_id, password)
es_connection = elasticsearch.Elasticsearch(hosts=hosts, port=port, http_auth=http_auth)

search_keyword = '2018-05-17_2018-05-18'

now_str = str(datetime.datetime.now())[:10]
headers = ['date_str', 'CSM_devID', 'csm_citys', 'csm_home', 'csm_mdu',
           'ott_citys', 'OTT_devID', 'ott_mac1', 'ott_mac2', 'ott_platform']
result_lst = []
search_body = {
    "query":{
        "bool":{
            "filter":[
                {"term": {"date_str": search_keyword}}]}}}

es_scan = elasticsearch.helpers.scan(es_connection, query=search_body,
                                     index='ott_csm_behavior_match_cross_date')

for line in es_scan:
    data_dic = line['_source']
    data_dic.pop('timestamp')
    detail_lst = data_dic['detail']
    data_dic.pop('detail')
    key_lst = []
    for detail_dic in detail_lst:
        detail_dic.pop('date')
        detail_dic.pop('timestamp')
        date_str = detail_dic['date_str']
        new_dic = {}
        for key, value in detail_dic.items():
            new_key = key + date_str
            new_dic[new_key] = value
            key_lst.append(new_key)
        copy_dic = copy.deepcopy(new_dic)
        data_dic = dict(data_dic, **copy_dic)
    result_lst.append(data_dic)
headers.extend(key_lst)
print('the length of %s is %s' % (search_keyword, len(result_lst)))
count = 1
while len(result_lst) > 0:
    csv_name = search_keyword + now_str + str(count) + '.csv'
    csv_file = open(csv_name, 'w')
    writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=headers)
    header_dic = {}
    for variable in headers:
        header_dic[variable] = variable
    writer.writerow(header_dic)
    for line in result_lst:
        writer.writerow(line)
    if len(result_lst) > 10000:
        result_lst = result_lst[10000:]
        count +=1
    else:
        break