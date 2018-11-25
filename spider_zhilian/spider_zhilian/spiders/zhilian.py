#写一个爬虫尝试爬取智联招聘
import scrapy
from scrapy.spiders import Spider,CrawlSpider
#添加去重
# from scrapy.dupefilters import RFPDupeFilter
#添加Rule,用于,匹配大量的网址
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

#导入item类
from spider_zhilian.items import SpiderZhilianItem
import json

#导入自己写的省份信息输出
from .multi_spider import crawler_zhilian,return_province_info
from .slave import manu_conn_redis1

#导入redis的分布式爬虫类
from scrapy_redis.spiders import RedisSpider

#就是,爬虫教程,有提及的,就是,最基本的爬虫,包括了
#item
#name
#start_urls
#parse(这个是后续的处理吧)


class zhiLianSpider(RedisSpider):
    name = "zhilian_1"

    def __init__(self):
        self.allowed_domains = ['zhaopin.com']
        start_urls = [
            'https://sou.zhaopin.com/?jl=489',
        ]
    
    rules = (
        Rule(LinkExtractor(allow=(r"https://fe-api.zhaopin.com/c/i/sou/\?cityId")),callback='handle_json_2_item',follow=True),
        Rule(LinkExtractor(allow=(r"https://sou.zhaopin.com/\?jl=489$")),callback='create_2_request',follow=True),
        
    )

    #redisSpider说,一定需要定义好parse函数,那没办法了,那就定义吧.
    def parse(self,response):
        pass
        for x in self.create_2_request(response):

            pass
        



#由于智联招聘现在的前端已经换了模式,所以需要采用特殊模式,直接当作是客户端处理

    def handle_json_2_item(self,response):
        #格式化内容,转换json变成dict
        #response里面有text方法的,不过大多数情况是使用xpath这个方法的,因为这个用途比较广泛
        pass
        response_dict = json.loads(response.text)
        items = SpiderZhilianItem()
        for x in response_dict['data']['results']:
            items['city_name'] =  x['city']['display']
            items['city'] = x['city']['items'][0]['code']
            items['company_name'] = x['company']['name']
            items['number'] = x['company']['number']
            
            items['education'] = x['eduLevel']['name']
            items['experience'] = x['workingExp']['name']
            items['salary'] = x['salary']
            items['job_name'] = x['jobName']
            yield items

    #创建批量的请求,
    #这里的话,还需要解析出具体的省份信息
    def create_2_request(self,response):
        #那需要获取省份信息的话,那就调用旁边的啦!.哈哈.提高利用率嘛.
        
        #这里就先假设是用热门城市来做了
        hot_city = return_province_info()['hot_citys']
        
        #制作大量url地址,又重新提交给scrapy
        #然后就是code和url配合
        redis_conn = manu_conn_redis1
        for x in hot_city:
            for x1 in crawler_zhilian(x['code']):
                for x2 in x1:
                    print(x2)
                    # yield redis_conn.lpush("zhilian_1:start_urls",x2)
                    # yield scrapy.Request(x2,callback=self.handle_json_2_item)


        