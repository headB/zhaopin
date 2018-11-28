from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from .multi_spider import conn_redis


conn_redis.lpush("51job:start_urls","https://search.51job.com/list/030200,000000,0000,00,9,99,%2520,2,1.html")

class w51jobCrawler(RedisCrawlSpider):

    name = '51job'
    
    rules = (
        #这个规则是捉取10个热门城市的首页信息
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='ht']//a")),callback='parse_items',follow=False),
        # Rule(LinkExtractor(restrict_xpaths=("//div[@class='ht']//@href")),callback='parse_items',follow=False),
        # Rule(LinkExtractor(allow=(r"51job\.com")),callback='parse_items',follow=False),
    )

    def __init__(self,*args,**kwargs):
        print("I am the kumanxuan")
        self.allowed_domains = ['51job.com']
        super().__init__(*args,**kwargs)

    
    def get_hot_city_info(self,response):
        pass
        print("xxcc")
        # print(dir(response))


    def parse_items(self,response):
        print("kumanxuan")
        pass

    # def 
    
    

