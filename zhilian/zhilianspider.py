# -*- coding:utf-8 -*-
# date:2017-7-13
# author:Alex

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import quote
from savedata import get_Mysql

class mySpider(object):
    def __init__(self,daname,mykey,mycity):
        self.dbname = daname
        self.key = mykey
        self.city = mycity
        self.start_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&p=1".format(quote(self.city), quote(self.key))
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8,mt;q=0.6",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"sou.zhaopin.com",
            "Referer":"http://www.zhaopin.com/",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
        }
        self.mysql = get_Mysql(self.dbname,self.key,self.city)
        self.mysql.create_table()

    # 获取一页的招聘信息,并判断是否有下一页的链接，递归爬取所有页的信息
    def get_one_html(self,url):
        html = requests.get(url,headers = self.headers).text
        soup = BeautifulSoup(html,"lxml")
        jobs = soup.select("#newlist_list_content_table > table")[1:]  #去掉标题信息
        for job in jobs:
            data = {}
            # 招聘链接
            data["job_link"] = job.find_all("td",attrs={"class":"zwmc"})[0].find("div").find("a").get("href")
            # 职位名称
            data["job_name"] = job.find_all("td",attrs={"class":"zwmc"})[0].text.strip()
            # 反馈率
            data["fk_lv"] = job.find_all("td",attrs={"class":"fk_lv"})[0].text.strip()
            # 公司名称
            data["gs_name"] = job.find_all("td",attrs={"class":"gsmc"})[0].text.strip()
            # 公司链接
            data["gs_link"] = job.find_all("td",attrs={"class":"gsmc"})[0].find("a").get("href")
            # 职位月薪
            data["job_gz"] = job.find_all("td",attrs={"class":"zwyx"})[0].text.strip()
            # 工作地点
            data["job_dd"] = job.find_all("td",attrs={"class":"gzdd"})[0].text.strip()
            # 发布日期
            data["create_date"] = job.find_all("td",attrs={"class":"gxsj"})[0].text.strip()
            # 公司性质
            gsxz = job.find_all("li",attrs={"class":"newlist_deatil_two"})[0].find_all("span")[1].text.strip()
            # 公司规模
            gsgm = job.find_all("li",attrs={"class":"newlist_deatil_two"})[0].find_all("span")[2].text.strip()
            # 学历/经验要求
            xlyq = job.find_all("li",attrs={"class":"newlist_deatil_two"})[0].find_all("span")[3].text.strip()
            try:
                data["gs_xz"] = gsxz.replace("公司性质：","")
            except:
                data["gs_xz"] = gsxz
            try:
                data["gs_gm"] = gsgm.replace("公司规模：","")
            except:
                data["gs_gm"] = gsgm
            if "学历" in xlyq:
                data["xlyq"] = xlyq.replace("学历：","")
            elif "经验" in xlyq:
                data["xlyq"] = xlyq.replace("经验：","")
            else:
                pass
                data["xlyq"] = xlyq
            # 职位简介
            data["job_infos"] = job.find_all("li",attrs={"class":"newlist_deatil_last"})[0].text.strip()
            print(data)
            self.mysql.insert_data(data)
        # 判断是否有下一页，如果有的话就继续爬信息，否则结束爬虫
        try:
            next_url = soup.select("li.pagesDown-pos > a")[0].get("href")
            pagenum = re.findall("&p=(\d+)",next_url)[0]
            print("成功获取下一页的链接，开始爬取第{}页的信息".format(pagenum))
        except:
            print("已经是最后一页了，所有职位信息已经提取完毕")
        else:
            self.get_one_html(next_url)

    def main(self):
        '''尝试爬信息并保存到数据库，若爬虫失败也要关闭数据库连接'''
        try:
            self.get_one_html(self.start_url)
        except Exception as e:
            print(e)
        finally:
            self.mysql.close_table()

if __name__ == '__main__':
    t = time.time()
    # 列表循环创建表格
    jobs = ["python"]
    citys = ["深圳","武汉"]
    for i in jobs:
        for j in citys:
            s = mySpider("zhilian_jobs",i,j)
            s.main()
    print("耗时：{:.2f}秒".format(float(time.time()-t)))

