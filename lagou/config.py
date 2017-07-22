# -*- coding:utf-8 -*-
# date:2017-7-11
# anthor:Alex

import time
import random
import datetime
import hashlib
from urllib.parse import quote

class myheaders(object):
        # 获取当前时间字符串
    T = datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M%S")
        # 获取当前时间戳
    t = str(int(time.time()))
    # 获取一个以时间为变动一句的加密参数，用来改变cookie中的SEARCH_ID，不过不知道这个值的具体算法，因此这个参数纯属于自己构造的
    k = hashlib.md5()
    k.update(t.encode("utf-8"))
    k = k.hexdigest()
    USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6"
]
    # 按照传入的搜索关键词和城市，形成可变动的headers
    @classmethod
    def get_headers(cls,mykey,mycity):
        headers = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8,mt;q=0.6",
            "Connection":"keep-alive",
            "Content-Length":"25",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Host":"www.lagou.com",
            "Origin":"https://www.lagou.com",
            "Referer":"https://www.lagou.com/jobs/list_{}?px=default&city={}".format(quote(mykey),quote(mycity)),
            "User-Agent":random.choice(cls.USER_AGENTS),
            "X-Anit-Forge-Code":"0",
            "X-Anit-Forge-Token":"None",
            "X-Requested-With":"XMLHttpRequest",
        }
        # 自定义一个cookie生成器，有一些参数的变化规则并不知道，但是可以构造自己的规则来变动，结果并不影响请求
        cookies = {
            "index_location_city":quote(mycity,encoding="utf-8"),
            "JSESSIONID":"ABAAABAAAIAACBI699C6AEC8D8F86B2D26DDF7C78A35B92",
            "_gat":"1",
            "LGRID":cls.T+"-dc4a4e99-662d-11e7-a781-5254005c3644",
            "user_trace_token":cls.T+"-629775c7f8c942c3a3eae9e5944c7af9",
            "LGSID":cls.T+"-d655caa6-662d-11e7-abc1-525400f775ce",
            "PRE_LAND":"https%3A%2F%2Fwww.lagou.com%2F",
            "TG-TRACK-CODE":"index_search",
            "_ga":"GA1.2.477538007."+cls.t,
            "LGUID":cls.T+"-4403d434-6565-11e7-a72a-5254005c3644",
            "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6":cls.t,
            "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6":cls.t,
            "_gid":"GA1.2.356832361."+cls.t,
            "SEARCH_ID":cls.k
        }
        c = ""
        for i in cookies:
            c += i+"="+cookies[i]+";"
        headers["cookie"] = c
        return headers


if __name__ == '__main__':
    '''测试'''
    h = myheaders.get_headers("python","深圳")
    print(h)

