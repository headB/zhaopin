from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from .multi_spider import conn_redis
import requests
import re
import json
from lxml import etree
from spider_zhilian.items import SpiderZhilianItem

#https://search.51job.com/list/010000,000000,0000,00,9,99,%2520,2,1.html
#格式是01000,第一串数字

#组装url,用于爬虫
def parse_url(city_code):

    return "https://search.51job.com/list/{},000000,0000,00,9,99,\%2520,2,1.html".format(city_code)




conn_redis.lpush("51job:start_urls",parse_url("030200"))

class w51jobCrawler(RedisCrawlSpider):

    name = '51job'
    start_urls = ""
    rules = (
        #这个规则是捉取10个热门城市的首页信息
        # Rule(LinkExtractor(restrict_xpaths=("//div[@class='ht']//a")),callback='test'),
        #这里就可以开始捉取合资格的url地址了.
        Rule(LinkExtractor(allow=("https://search\.51job\.com/list")),callback='parse_page'),
    )

    def __init__(self,*args,**kwargs):
        
        self.allowed_domains = ['51job.com']
        super().__init__(*args,**kwargs)
        # self.city_code = self.parse_city_code()
        self.get_hot_city_info()

    
    def get_hot_city_info(self):
        
        city_code = self.parse_city_code()
        # print(response.url)
        del(city_code['广州'])
        enter_url = parse_url("030200")
        response = etree.HTML(requests.get(enter_url).content.decode("GBK"))
        
        #获取热门城市的中文名字
        #然后可以提交到redis
        for x in response.xpath("//div[@class='ht']//a"):
            try:
                x1 = city_code[x.text]
                conn_redis.lpush("51job:start_urls",parse_url(x1))
            except Exception as e:
                print(e)
                
        


        #然后没解析出一个城市的url都lpush到redis数据库当中!
        # conn_redis.lpush("51job:start_urls",response.url)

   

    def parse_page(self,response):

        print("checking")

        for x in self.w51jobCommonItem(response):

            yield x


    def parse_city_code(self):

        #获取js,全国地区城市的代码
        url = "https://js.51jobcdn.com/in/js/2016/layer/area_array_c.js?20180319"
        code_html = re.findall("\{.+\}",requests.get(url).content.decode("GBK").replace("\r\n",''))[0]
        # code_html = requests.get(url).content.decode("GBK")
        #然后直接转换成为字典
        dict1 = {}
        code_dict = json.loads(code_html)
        # print(code_dict)
        for x,y in code_dict.items():
            dict1[y] = x

        return dict1

    #这里可以处理
    #处理每一个首页的职位信息
    def parse_start_url(self,response):

        for x in  self.w51jobCommonItem(response):
            yield x


    def w51jobCommonItem(self,response):

        for x in response.xpath("//div[@class='dw_table']//div[@class='el']"):

            items = SpiderZhilianItem()
            try:

                #还有城市代码
                items['city'] = re.findall("list/(.+?),",response.url)[0]
                #职位名称
                items['job_name'] = x.xpath("p[@class='t1 ']/span/a/text()").extract()[0].strip("\r\n").strip()
                #公司名
                items['company_name'] = x.xpath("span[@class='t2']/a/text()").extract()[0].strip("\r\n").strip()
                # #工作地点
                items['city_name'] = x.xpath("span[@class='t3']/text()").extract()[0].strip("\r\n").strip()
                # #薪资
                items['salary'] = x.xpath("span[@class='t4']/text()").extract()[0].strip("\r\n").strip()
            except Exception as e:
                print(e)
        
            yield items

    

