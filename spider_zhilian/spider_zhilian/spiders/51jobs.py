from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from .multi_spider import conn_redis


conn_redis.lpush("51job:start_urls","https://search.51job.com/list/030200,000000,0000,00,9,99,%2520,2,1.html")

class w51jobCrawler(RedisCrawlSpider):

    name = '51job'
    
    rules = (
        Rule(LinkExtractor(allow=(r'51job\.com')),callback='parse_items',follow=True),
    )

    def __init__(self,*args,**kwargs):
        print("I am the kumanxuan")
        self.allowed_domains = ['51job.com']
        super().__init__(*args,**kwargs)

    


    def parse_items(self,response):
        print("kumanxuan")
        pass

    

