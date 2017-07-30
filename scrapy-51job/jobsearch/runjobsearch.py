from scrapy import cmdline
# 只运行，不输出文件，当已经设置了数据保存的pipelines的时候使用
cmdline.execute('scrapy crawl jobinfos'.split())

# 输出为CSV格式，但是有空格的就会出错，所以不推荐
# cmdline.execute('scrapy crawl Tieba -o info.csv -t csv'.split())

# 输出为json格式
# cmdline.execute('scrapy crawl Tieba -o item.json'.split())
