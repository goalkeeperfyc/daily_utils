# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 11:26:08 2018

在Excel里完成半/全角逗号的替换

@author: goalkeeperfyc
"""


import jieba
import pandas as pd


#jieba.load_userdict('D:/CSM3.0/经典咏流传-弹幕研究/new words/added words.txt')
#jieba.load_userdict('D:/CSM3.0/经典咏流传-弹幕研究/new words/elementofprogram.txt')
#jieba.load_userdict('D:/CSM3.0/经典咏流传-弹幕研究/new words/nickname.txt')
#jieba.load_userdict('D:/CSM3.0/经典咏流传-弹幕研究/new words/specialsentence.txt')
#jieba.load_userdict('D:/CSM3.0/经典咏流传-弹幕研究/new words/styleofwatching.txt')


def csv_to_lst_with_headline(csvname):
    result_lst = []
    openfile = open(csvname, 'r', encoding='gb18030')
    head = openfile.readline()
    head = head.replace('\n', '')
    head_lst = head.strip().split(',')
    for line in openfile:
        line = line.replace('\n', '')
        line_lst = line.strip().split(',')
        test_dict = dict(zip(head_lst,line_lst))
        result_lst.append(test_dict)
    return result_lst

def cut_word(file_name):
    task_lst = csv_to_lst_with_headline(csvname=file_name)
    result_lst = [] 
    for task in task_lst:
        task_str = task['content']
        seg_lst = jieba.lcut(task_str)
        task['seg_result'] = seg_lst
        result_lst.append(task)
    return result_lst

def count_word(task_lst):
    word_lst = []
    word_dic = {}
    for task in task_lst:
        if task not in word_lst:
            word_dic[task] = 1
            word_lst.append(task)
        else:
            word_dic[task] += 1
    result_lst = []
    for key, value in word_dic.item:
        D0 = {'count':value,'word':key}
        result_lst.append(D0)
    return result_lst

def output_result(lst_name, csv_name):
    df = pd.DataFrame(lst_name)
    df.to_csv(csv_name, index=False, encoding='gb18030')


if __name__=='__main__':
    file_name = 'absolute path' #such as 'D:\fangyucheng\answer_to_question.csv'
    cut_result = cut_word(file_name)
    csv_name1 = 'output csv name' #this is to output the result of cutting word
    output_result(lst_name=cut_result, csv_name=csv_name1)
    count_task_lst = []
    for line in cut_result:
        cut_lst = line['seg_result_result']
        count_task_lst.extend(cut_lst)
    count_result = count_word(task_lst=count_task_lst)
    csv_name2 = 'absolute path' #same as above. This is to output the result of counting word
    output_result(lst_name=count_result, csv_name=csv_name2)
    