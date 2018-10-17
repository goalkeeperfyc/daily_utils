# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 13:49:55 2018

@author: fangyucheng
"""

import urllib
import requests
import hashlib
from crawler_sys.utils.output_results import retry_get_url


class Crawler_kwat():

    def releaser_page(releaerUrl):

        post_dic = {'token': '',
                    'user_id': '2228125',
                    'lang': 'zh',
                    'count': 30,
                    'privacy': 'public',
                    'referer': 'ks://profile/2228125/5200531675520421301/1_i/1614100635136053248_h236/8',
                    'os': 'android',
                    'client_key': '3c2cd3f3',
                    'sig': 'd01d346906fe6f1681c579a3c24fa3ba'}

        headers= {'Connection': 'keep-alive',
                  'Accept-Language': 'zh-cn',
                  'User-Agent': 'kwai-android',
                  'X-REQUESTID': '4000022',
                  'Content-Type': 'application/x-www-form-urlencoded',
                  'Content-Length': '218',
                  'Host': 'api.ksapisrv.com',
                  'Accept-Encoding': 'gzip'}
        
        #post_parameter = 
        
        post_url = ('http://api.ksapisrv.com/rest/n/feed/profile2?app=0&'
                    'lon=116.471016&c=MYAPP&sys=ANDROID_4.4.4&mod=Netease(MuMu)'
                    '&did=ANDROID_54767d8bf41ac9a4&ver=5.2&net=WIFI'
                    '&country_code=CN&appver=5.2.1.4701&oc=UNKNOWN&ftt='
                    '&ud=0&language=zh-cn&lat=39.907898')

        get_page = requests.post(post_url, headers=headers, data=post_dic)
        page_dic = get_page.json()