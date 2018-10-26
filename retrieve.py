#!/usr/bin/python

import cgi
import datetime
import copy
import elasticsearch
import elasticsearch.helpers
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
print (sys.getdefaultencoding())

form = cgi.FieldStorage()
print("Content-type: text/html\n")

html = """
<title>Start Downloading</title>
<h1>Downloading</h1>
<hr>
<p>The input date span is: %s</p>
<p>we are trying to download the data you wanted</p>
<hr>"""

search_keyword = form['date'].value

print(html % search_keyword)

hosts = '192.168.17.11'
port = 80
user_id = 'fangyucheng'
password = 'VK0FkWf1fV8f'
http_auth = (user_id, password)
es_connection = elasticsearch.Elasticsearch(hosts=hosts, port=port, http_auth=http_auth)

csv_path = "/home/fangyucheng/cross_date_result/"

now_str = str(datetime.datetime.now())[:10]
headers = ['date_span', 'CSM_devID', 'csm_citys', 'csm_home', 'csm_mdu',
           'OTT_devID', 'ott_citys', 'ott_mac1', 'ott_mac2', 'ott_platform',
           'date_str', 'csm_viewLen', 'ott_viewLen',
           'vector_dist', 'vector_cos', 'viewLen_ott_over_csm', ]
result_lst = []

search_body = {
    "query":{
        "bool":{
            "filter":[
                {"term": {"date_str": search_keyword}}]}}}

print("<p>Initialization finished</p>")

es_scan = elasticsearch.helpers.scan(es_connection, query=search_body,
                                     index='ott_csm_behavior_match_cross_date')

print("<p>start downloading</p>")

for line in es_scan:
    data_dic = line['_source']
    date_span = data_dic['date_str']
    data_dic['date_span'] = date_span
    data_dic.pop('date_str')
    detail_lst = data_dic['detail']
    data_dic.pop('detail')
    for detail_dic in detail_lst:
        detail_dic.pop('date')
        detail_dic.pop('timestamp')
        data_dic = dict(data_dic, **detail_dic)
        result_lst.append(data_dic)

print("<p>Got data from es start to export</p>")
print('the length of %s is %s' % (search_keyword, len(result_lst)))
count = 1
while len(result_lst) > 0:
    csv_name = csv_path + search_keyword + now_str + str(count) + '.csv'
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
