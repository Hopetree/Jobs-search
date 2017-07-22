## 拉钩网招聘信息提取爬虫</br>
### 目标网站 https://www.lagou.com/
- 项目运行
</br>启动lagouspider.py填写要查询的城市和关键词即可，爬虫运行完毕会将信息保存到Excel表格中，
表格名称以启动时间和关键词命名
- 项目结构
    - lagouspider.py
    </br>主爬虫文件，负责调度其他文件执行信息的提取和数据保存
    - savedata.py
    </br>信息保存文件，负责信息保存的方式
    - config.py
    </br>配置文件，本项目中主要负责构造headers
- Python库支持
<br>`requests` 
`json`
`BeautifulSoup`
`urllib.parse`
`xlwt`
`hashlib`
`datetime`
`random`
- spider思路
</br>请求一次获取总页码数>>前提并保存数据到Excel>>按照总页码数循环翻页
- 其他
</br>请求头headers需要附带cookie参数，可以自己构建一个cookie函数自动生成

