# -*- coding: utf-8 -*-

import scrapy
import re
from urllib.parse import quote
from scrapy.conf import settings
from jobsearch.items import JobsearchItem

class Jobinfospider(scrapy.Spider):
    name = 'jobinfos'
    allowed_domains = ['jobs.51job.com','search.51job.com']
    start_urls = ['http://search.51job.com']

    def parse(self, response):
        baseurl = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea={}&keyword={}&keywordtype=2&' \
                  'lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'
        city_dict = settings['CITY_DICT']
        jobname = settings['JOBNAME']
        citys = settings['CITYS']
        if len(citys) == 1:
            self.logger.info("搜索城市为：{}".format(citys[0]))
            citynum = city_dict[citys[0]]
        elif len(citys) > 1:
            self.logger.info("搜索城市为：{}".format("&".join(citys)))
            lis = [city_dict[c] for c in citys]
            citynum = ",".join(lis)
        else:
            self.logger.info("未选择城市，搜索城市为：全国")
            citynum = ""
        the_url = baseurl.format(quote(citynum),quote(jobname))
        for each_url in [the_url]:
            yield scrapy.Request(url=each_url,callback=self.parse_urls)

    def parse_urls(self,response):
        job_urls = response.xpath('//*[@id="resultList"]/div/p/span/a')
        for each in job_urls:
            job_url = each.xpath('@href').extract_first()
            yield scrapy.Request(url=job_url,callback=self.parse_infos)
        # 翻页规则
        next_url = response.xpath('//li[@class="bk"]/a[contains(text(),"下")]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=next_url,callback=self.parse_urls)

    def parse_infos(self,response):
        item = JobsearchItem()
        item['job_link'] = response.url
        item['job_name'] = response.xpath('//div[@class="cn"]/h1/@title').extract_first()
        item['job_city'] = response.xpath('//div[@class="cn"]/span[@class="lname"]/text()').extract_first()
        item['salary'] = response.xpath('//div[@class="cn"]/strong/text()').extract_first()
        item['gs_name'] = response.xpath('//div[@class="cn"]/p[@class="cname"]/a/@title').extract_first()
        item['gs_link'] = response.xpath('//div[@class="cn"]/a/@href').extract_first()
        msg = response.xpath('//p[contains(@class,"msg") and contains(@class,"ltype")]/text()').extract_first().strip()
        item['gs_msg'] = re.sub("\s","",msg)
        item['gs_fl'] = response.xpath('//p[@class="t2"]/span/text()').extract()
        # 学历要求，可能不存在，这个必须先找到子节点，然后往回找父节点
        item['req_xl'] = response.xpath('//em[@class="i2"]/../text()').extract_first()
        # 经验要求，可能不存在
        item['req_jy'] = response.xpath('//em[@class="i1"]/../text()').extract_first()
        item['create_date'] = response.xpath('//em[@class="i4"]/../text()').extract_first()
        infos = response.xpath('//div[contains(@class,"job_msg")]/text()').extract()
        item['job_info'] = re.sub("\s","","".join(infos))
        address = response.xpath('//p[@class="fp"]/text()').extract()
        item['address'] = re.sub("\s","","".join(address))

        yield item

