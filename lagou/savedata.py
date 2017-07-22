# -*- coding:utf-8 -*-
# date:2017-7-11
# anthor:Alex

'''字体和背景色代号可见测试文件https://github.com/Hopetree/mytests/tree/master/excel-module'''

import xlwt
import datetime

class myexcel(object):
    def __init__(self,key,city):
        self.key = key
        self.city = city
        # 获取当前时间并生成时间字符串用来给表格命名
        self.T = datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M")
        # 创建一个工作簿和一个sheet表格
        self.work = xlwt.Workbook(encoding="utf-8")
        self.sheet = self.work.add_sheet("{}_{}".format(self.key,self.city))
        # 表格自带标题
        self.get_title()

    # 设置表格标题和列宽
    def get_title(self):
        # 设置字体
        font = xlwt.Font()
        # font.name = "Arial"    #字体名称
        font.colour_index = 1  # 颜色为白色
        font.bold = True  # 字体加粗
        font.height = 20 * 11  # 字体决定了行高，后面一个数字可以决定字体型号
        # 设置背景色
        patterni = xlwt.Pattern()
        patterni.pattern = xlwt.Pattern.SOLID_PATTERN
        patterni.pattern_fore_colour = 24  #一种类似天蓝色

        # 设置风格
        style = xlwt.XFStyle()
        style.font = font
        style.pattern = patterni

        for r,title in zip(range(12),["城市","职位","公司全称","待遇","经验要求","学历要求","办公地点","公司规模","职位吸引力",
                                      "融资轮次","发布时间","招聘链接"]):
            self.sheet.write(0,r,title,style)

        for x in [0,3,4,5,6,7,9]:
            self.sheet.col(x).width = 256*8
        self.sheet.col(1).width = 250*16
        self.sheet.col(2).width = 256*30
        self.sheet.col(8).width = 256*40
        self.sheet.col(10).width = 256*20
        self.sheet.col(11).width = 256*50

    # 以列表的形式，i是行参数，每一行插入一个信息
    def writeinfos(self,i,data):
        self.sheet.write(i,0,data["city"])
        self.sheet.write(i,1,data["positionName"])
        self.sheet.write(i,2,data["companyFullName"])
        self.sheet.write(i,3,data["salary"])
        self.sheet.write(i,4,data["workYear"])
        self.sheet.write(i,5,data["education"])
        self.sheet.write(i,6,data["district"])
        self.sheet.write(i,7,data["companySize"])
        # 有的信息不存在这个key所以要判断一下信息的完整性避免报错
        lis = data["companyLabelList"]
        if len(lis) > 0:
            s = ",".join(lis)
        else:
            s = "None"
        self.sheet.write(i,8,s)
        self.sheet.write(i,9,data["financeStage"])
        self.sheet.write(i,10,data["createTime"])
        link = "https://www.lagou.com/jobs/{}.html".format(data["positionId"])
        self.sheet.write(i,11,link)

    # 信息插入完毕之后保存表格，在主爬虫完成之后必须调用这个函数才能保存表格
    def save_excel(self):
        self.work.save("{}_{}_{}.xls".format(self.T,self.key,self.city))


