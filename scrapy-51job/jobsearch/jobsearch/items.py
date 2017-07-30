# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_link = scrapy.Field()     # 招聘链接1
    job_name = scrapy.Field()     # 职位名称2
    salary = scrapy.Field()       # 薪酬3
    gs_name= scrapy.Field()       # 公司名称4
    job_city = scrapy.Field()     # 工作城市5
    gs_msg = scrapy.Field()       # 公司规模6
    gs_fl = scrapy.Field()        # 公司福利7
    req_xl = scrapy.Field()       # 学历要求8
    create_date = scrapy.Field()  # 发布时间9
    job_info = scrapy.Field()     # 职位信息10
    address = scrapy.Field()      # 办公地点11
    gs_link = scrapy.Field()      # 公司链接12
    req_jy = scrapy.Field()       # 经验要求13



