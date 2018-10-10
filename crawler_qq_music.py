# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 09:26:59 2018

@author: fangyucheng
"""

import requests 
from bs4 import BeautifulSoup


def process_one_song(line):
    song = line.find('span', {'class': 'songlist__songname_txt'}).text
    song = song.replace('\n', '').replace('\r', '').replace('\t', '')
    singer = line.find('div', {'class': 'songlist__artist'}).text
    singer = singer.replace('\n', '').replace('\r', '').replace('\t', '')
    album = line.find('div', {'class': 'songlist__album'}).text
    album = album.replace('\n', '').replace('\r', '').replace('\t', '')
    duration = line.find('div', {'class': 'songlist__time'}).text
    duration = duration.replace('\n', '').replace('\r', '').replace('\t', '')
    return {'song': song,
            'singer': singer,
            'album': album,
            'duration': duration}

def qq_music(url):
    result_lst = []
    get_page = requests.get(url)
    get_page.encoding = 'utf-8'
    page = get_page.text
    soup = BeautifulSoup(page, 'html.parser')
    song_lst = soup.find('ul', {'class': 'songlist__list'})
    for line in song_lst:
        try:
            song_dic = process_one_song(line)
            result_lst.append(song_dic)
            print('get_one_line')
        except:
            pass
    return result_lst


if __name__ == '__main__':
    url = 'https://y.qq.com/n/yqq/playlist/5242521064.html#stat=y_new.profile.create_playlist.click&dirid=13'
    result = qq_music(url)