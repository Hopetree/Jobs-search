# -*- coding:utf-8 -*-
# date:2017-7-15
# author:Alex

import pymysql
import datetime

class get_mysql(object):
    '''链接数据库，并根据提供的数据库名称和关键词信息创建一个表格，表格存在就不创建'''
    def __init__(self,dbname,key,citys):
        self.T = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M")
        self.dbname = dbname
        self.key = key
        if len(citys) == 1:
            self.city = citys[0]
        elif len(citys) > 1:
            self.city = "&".join(citys)
        else:
            self.city = ""
        self.table_name = "{}_{}_{}".format(self.T,self.key,self.city)
        self.conn = pymysql.Connect(
            host="localhost",
            port=3306,
            user='root',
            password='python',
            db=self.dbname,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        # 直接创建一个表格
        self.create_table()

    # 创建表格的函数，表格名称按照时间和关键词命名
    def create_table(self):
        sql = '''CREATE TABLE `{tbname}`(
        {job_name} varchar(100) not null,
        {gs_name} varchar(100),
        {salary} char(20),
        {job_site} char(20),
        {create_date} char(20),
        {job_link} varchar(100),
        {gs_link} varchar(100)
        )'''
        try:
            self.cursor.execute(sql.format(tbname=self.table_name,job_name="职位名称",gs_name="公司名称",salary="薪资",
                                       job_site="工作地点",create_date="发布时间",job_link="招聘链接",gs_link="公司链接"))
        except Exception as e:
            print("创建表格失败，表格可能已经存在！",e)
        else:
            self.conn.commit()
            print("成功创建一个表格，名称是{}".format(self.table_name))

    # 插入信息函数，每次插入一条信息，插入信息失败会回滚
    def insert_data(self,data):
        '''插入数据，不成功就回滚操作'''
        sql = '''INSERT INTO `{}` VALUES('{}','{}','{}','{}','{}','{}','{}')'''
        try:
            self.cursor.execute(sql.format(self.table_name,data["job_name"],data["gs_name"],data["salary"],data["job_site"],
                                           data["create_date"],data["job_link"],data["gs_link"]))
        except Exception as e:
            self.conn.rollback()
            print("插入信息失败，原因：",e)
        else:
            self.conn.commit()
            print("成功插入一条信息")

    def close_mytable(self):
        '''关闭游标和断开链接，数据全部插入后必须执行这个操作'''
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    data = {'gs_name': '深圳市东健宇电子有限公司', 'job_link': 'http://jobs.51job.com/shenzhen/86494101.html?s=01&t=0', 'job_site': '深圳', 'salary': '4.5-6千/月', 'gs_link': 'http://jobs.51job.com/all/co2628963.html', 'job_name': '淘宝/天猫运营', 'create_date': '07-15'}
    m = get_mysql("51job","爬虫",["深圳","武汉"])
    m.create_table()
    m.insert_data(data)

