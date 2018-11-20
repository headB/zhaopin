#写一个爬虫尝试爬取智联招聘

from scrapy import Spider
#添加去重
# from scrapy.dupefilters import RFPDupeFilter


#就是,爬虫教程,有提及的,就是,最基本的爬虫,包括了
#item
#name
#start_urls
#parse(这个是后续的处理吧)

class zhiLianSpider(Spider):
    name = "zhilian_1"
    allowed_domains = ['zhaopin.com']
    start_urls = [
        'https://sou.zhaopin.com/?jl=489',
    ]

    def parse(self,response):

        pass
        print("捉到我一次!")
        print(response)

        #然后就可以写规则了.
        