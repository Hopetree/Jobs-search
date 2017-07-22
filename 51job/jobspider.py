# -*- coding:utf-8 -*-
# date:2017-7-15
# author:Alex

'''
前程无忧网招聘信息爬虫
'''

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from citynum import city_to_num
from savedata import get_mysql


class Myspider(object):
    def __init__(self,dbname,mykey,mycitys):
        '''链接数据库并自动生成一个表格'''
        self.dbname = dbname
        self.key = mykey
        self.citys = mycitys
        self.Headers ={
            "Host": "search.51job.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
        }
        # 获取城市代码
        citynum = city_to_num.get_citynum(self.citys)
        # 起始链接，其中城市要用城市代码
        self.start_url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea={}&keyword={}&keywordtype" \
                         "=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9".format(quote(citynum),quote(self.key))
        self.mysql = get_mysql(self.dbname,self.key,self.citys)

    def get_one_page(self,url):
        '''从第一页开始，获取信息，并判断是否有下一页，如若有则继续爬虫，递归翻页'''
        req = requests.get(url,headers=self.Headers)
        req.encoding = "gbk"
        soup = BeautifulSoup(req.text,"lxml")
        # 获取所有职位信息，第一条是标题
        jobs = soup.select("#resultList > div.el")[1:]
        for job in jobs:
            data = {}
            data["job_name"] = job.select("p.t1")[0].text.strip()
            data["job_link"] = job.select("p.t1 > span > a")[0].get("href")
            data["gs_name"] = job.select("span.t2")[0].text.strip()
            data["gs_link"] = job.select("span.t2 > a")[0].get("href")
            data["job_site"] = job.select("span.t3")[0].text.strip()
            data["salary"] = job.select("span.t4")[0].text.strip()
            data["create_date"] = job.select("span.t5")[0].text.strip()
            print(data)
            self.mysql.insert_data(data)
        try:
            next_url = soup.select("li.bk")[-1].select("a")[0].get("href")
            pagenum = re.findall(",(\d+)\.html",next_url)[0]
            print("获取下一页的链接，开始爬取第{}页的信息".format(pagenum))
            self.get_one_page(next_url)
        except:
            print("无法获取下一页的链接，想必已经爬到了最后一页了，爬虫即将结束")

    def main(self):
        '''尝试爬信息并保存到数据库，若爬虫失败也要关闭数据库连接'''
        try:
            self.get_one_page(spider.start_url)
        except Exception as e:
            print(e)
        finally:
            self.mysql.close_mytable()


if __name__ == '__main__':
    t = time.time()
    dbname = "51job"
    KEY = "爬虫"
    # 城市使用一个列表，因为前程无忧可以一次多选城市查询
    CITYS = ["深圳","武汉"]
    spider = Myspider(dbname,KEY,CITYS)
    spider.main()
    print("耗时：{:.2f}秒".format(float(time.time() - t)))






