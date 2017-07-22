# -*- coding:utf-8 -*-
# date:2017-7-13
# author:Alex

import pymysql
import datetime

class get_Mysql(object):
    def __init__(self,dbname,key,city):
        self.dbname = dbname
        self.T = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M")
        # 数据库表格的名称
        self.table_name = "{}_{}_{}".format(self.T,key,city)
        # 链接数据库
        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user='root',
            password='python',
            db=self.dbname,
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.conn.cursor()

    def create_table(self):
        '''创建表格，创建失败就不创建了'''
        sql = '''CREATE TABLE `{tbname}` (
        {job_name} varchar(120) not null,
        {gs_name} varchar(120),
        {fk_lv} char(10),
        {job_gz} varchar(30),
        {job_dd} char(30),
        {gs_xz} char(20),
        {gs_gm} char(20),
        {xlyq} char(20),
        {create_date} char(25),
        {job_link} varchar(200),
        {gs_link} varchar(250),
        {job_infos} varchar(250)
        )'''
        try:
            self.cursor.execute(sql.format(tbname=self.table_name,job_name="职位名称",gs_name="公司名称",fk_lv="反馈率",job_gz="职位月薪",
                                           job_dd="公司地址",gs_xz="公司性质",gs_gm="公司规模",xlyq="学历经验",create_date="发布时间",
                                           job_link="招聘链接",gs_link="公司链接",job_infos="招聘简介"))
        except Exception as e:
            print("创建新的表格失败，原因：",e)
        else:
            self.conn.commit()
            print("创建了一个新的表格,名称是{}".format(self.table_name))

    def insert_data(self,data):
        '''插入数据，执行插入语句失败就回滚，执行成功才提交'''
        sql = '''INSERT INTO `{tbname}` VALUES('{job_name}','{gs_name}','{fk_lv}','{job_gz}','{job_dd}','{gs_xz}','{gs_gm}','{xlyq}',
        '{create_date}','{job_link}','{gs_link}','{job_infos}')'''
        try:
            self.cursor.execute(sql.format(tbname=self.table_name,job_name=data["job_name"],gs_name=data["gs_name"],
                                           fk_lv=data["fk_lv"],job_gz=data["job_gz"],job_dd=data["job_dd"],gs_xz=data["gs_xz"],gs_gm=data["gs_gm"],
                                           xlyq=data["xlyq"],create_date=data["create_date"],job_link=data["job_link"],
                                           gs_link=data["gs_link"],job_infos=data["job_infos"]))
        except Exception as e:
            self.conn.rollback()
            print("插入数据失败，原因：",e)
        else:
            self.conn.commit()
            print("插入一条数据成功")

    # 关闭游标和连接
    def close_table(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    data = {'fk_lv': '57%', 'create_date': '昨天', 'job_infos': '工作简介', 'job_dd': '深圳', 'job_link': 'http://jobs.zhaopin.com/280882811250068.htm', 'gs_xz': '民营', 'job_gz': '10001-15000', 'xlyq': '3-5年', 'gs_link': 'http://company.zhaopin.com/P2/CC2808/8281/CC280882811.htm', 'job_name': 'Python工程师（爬虫方向）+包住宿+周末双休+五险一金', 'gs_gm': '100-499人', 'gs_name': '深圳市中源航空服务有限公司'}


    ms = get_Mysql("zhilian_jobs","测试key","测试city")
    ms.create_table()
    ms.insert_data(data)
    ms.close_table()

