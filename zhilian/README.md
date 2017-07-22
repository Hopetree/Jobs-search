## 智联招聘网站招聘信息提取爬虫</br>
### 目标网站 http://www.zhaopin.com/
- 项目结构
    - zhilianspider.py
    </br>主爬虫文件，负责调度其他文件爬取信息和保存信息
    - savedata.py
    </br>保存信息文件，负责链接数据库和存储信息
    - Python库支持
    </br>`requests`
`BeautifulSoup`
`re`
`urllib.parse`
`pymysql`
- spider思路
</br>提取第一页信息>>提取并保存信息到数据库>>获取下一页链接>>递归翻页爬取
- 技巧与难点
</br>爬虫很简单，详情见代码和注释
- 数据样本见附件表格

  
