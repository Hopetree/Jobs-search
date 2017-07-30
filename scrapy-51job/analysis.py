# -*- conding:utf-8 -*-

import pymongo
import pandas as pd
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread


# 定义一个词语集合
set = set()

def get_infos():
    '''链接数据库，提取需要的信息，返回一个列表'''
    coon = pymongo.MongoClient(host='localhost', port=27017)
    db = coon['spiderdata']
    table = db['Python深圳7-30']
    df = pd.DataFrame(list(table.find()))
    infos = df.job_info.values
    return list(infos)

def get_word(lis,fla,word_num):
    '''接受3个参数，第一个是要提取词的列表，第二是需要提取的词性,第三个是要提取的词数'''
    del_words = ["工作","相关"]
    word_dict = {}
    for each in lis:
        word_list = jieba.posseg.cut(each)
        for each_word in word_list:
            # 英文词性需要单独处理，不能让大小写影响统计结果
            if fla == 'eng':
                theword = each_word.word.title() # 都将首字母大写其他小写
            else:
                theword = each_word.word
            theflag = each_word.flag  # 词性
            # 只提取名词
            if theflag == fla:
                if theword in set:
                    word_dict[theword] += 1
                else:
                    word_dict[theword] = 1
                    set.add(theword)
    # print(word_dict)
    LIST = sorted(word_dict.items(),key=lambda a:a[1],reverse=True)
    # print(LIST)
    return LIST[0:word_num]

def get_wc(word_dic,fontname,savename,photoname):
    '''传入4个参数，词频字典，字体文件，保存名称，图片样品名称'''
    colors = imread(photoname)
    wc = WordCloud(background_color='white', mask=colors, font_path=fontname, max_font_size=150)
    wc.generate_from_frequencies(word_dic)
    plt.imshow(wc)
    plt.axis('off')
    wc.to_file(savename)
    print('get the photo {} !'.format(savename))

def test():
    '''词性测试'''
    lis = "链接数据库，提取需要的信息，返回一个列表，MySQL和mongodb"
    words = jieba.posseg.lcut(lis)
    for e in words:
        print(e)

if __name__ == '__main__':
    # test()
    infos = get_infos()
    word_dic = dict(get_word(infos,'eng',150))

    get_wc(word_dic,r'docs\times.ttf','wordcloud.png',r'docs\github.jpg')

