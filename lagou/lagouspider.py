# -*- coding:utf-8 -*-
# date:2017-7-11
# anthor:Alex

'''
拉钩网爬虫，按照职业关键词和城市为主要参数提取信息
文件分为3块，本文件是爬虫块，负责主要爬虫功能；
Setting.py是设置文件，主要负责构造headers；
Savedata.py是数据处理文件，负责将提取到数据存储到（Excel表格）数据库中
'''

import requests
import json
from urllib.parse import quote
from config import myheaders
from bs4 import BeautifulSoup
from savedata import myexcel

class myspider(object):
    def __init__(self,mykey,mycity):
        # 自定义一个变量self.i，代表Excel表格的行数
        self.i = 1
        self.key = mykey
        self.city = mycity
        # 获取自定义请求头
        self.headers = myheaders.get_headers(mykey,mycity)
        # 获取表格类
        self.excel = myexcel(mykey,mycity)

    # 请求源代码，获取总页码数
    def get_pages(self):
        url = "https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput=".format(self.key,self.city)
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
        html = requests.get(url,headers=headers).text
        soup = BeautifulSoup(html,"lxml")
        totalnum = int(soup.select("span.totalNum")[0].text.strip())
        return totalnum

    # 获取单个页面的信息
    def get_one_html(self,pagenum):
        url = "https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false".format(quote(self.city))
        data = {
            "first":"true",
            "pn":pagenum,
            "kd":self.key
        }
        html = requests.post(url=url,headers=self.headers,data=data).text
        infos = json.loads(html)
        jobs = infos["content"]["positionResult"]["result"]
        for each in jobs:
            self.excel.writeinfos(self.i,each)
            self.i += 1

    # 循环获取所有页面的信息
    def main(self):
        nums = self.get_pages()
        for n in range(1,nums+1):
            self.get_one_html(n)
            print("总计{}页职位信息，已经成功写入{}页的信息到表格".format(nums,n))
        self.excel.save_excel()
        print("所有信息保存完毕！")

if __name__ == '__main__':
    # 城市为空的时候代表全国
    spider = myspider("Python","深圳")
    spider.main()