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

#就是,爬虫教程,有提及的,就是,最基本的爬虫,包括了
#item
#name
#start_urls
#parse(这个是后续的处理吧)


class zhiLianSpider(CrawlSpider):
    name = "zhilian_1"
    allowed_domains = ['zhaopin.com']
    start_urls = [
        'https://sou.zhaopin.com/?jl=489',
    ]
    
    rules = (
        Rule(LinkExtractor(allow=(r"https://fe-api.zhaopin.com/c/i/sou/\?cityId")),callback='handle_json_2_item',follow=True),
        Rule(LinkExtractor(allow=(r"https://sou.zhaopin.com/\?jl=489$")),callback='create_2_request',follow=True),
        
    )


#由于智联招聘现在的前端已经换了模式,所以需要采用特殊模式,直接当作是客户端处理

    def handle_json_2_item(self,response):
        #格式化内容,转换json变成dict
        #response里面有text方法的,不过大多数情况是使用xpath这个方法的,因为这个用途比较广泛
        pass
        response_dict = json.loads(response.text)
        items = SpiderZhilianItem()
        for x in response_dict['data']['results']:
            items['city_name'] =  x['city']
            items['city'] = x['city']['items'][0]
            items['company_name'] = x['company']['name']
            items['number'] = x['company']['number']
            items['number'] = x['number']
            yield items

    #创建批量的请求,
    #这里的话,还需要解析出具体的省份信息
    def create_2_request(self,response):
        #那需要获取省份信息的话,那就调用旁边的啦!.哈哈.提高利用率嘛.
        
        #这里就先假设是用热门城市来做了
        hot_city = return_province_info()['hot_citys']
        
        #制作大量url地址,又重新提交给scrapy
        #然后就是code和url配合
        for x in hot_city:
            for x1 in crawler_zhilian(x['code']):
                for x2 in x1:
                    yield scrapy.Request(x2,callback=self.handle_json_2_item)





    def process_job_info(self,response):
        # pass
        #尝试每一个结果,提取里面的关键字,例如是,职位,公司名称,薪资.
        # print(request_url_organize())
        items = SpiderZhilianItem()
        items['job_name'] = response.xpath(r"//div//span[@class='contentpile__content__wrapper__item__info__box__jobname__title']//text()").extract_first()
        items['salary'] = response.xpath(r"//div//p[@class='contentpile__content__wrapper__item__info__box__job__saray']//text()").extract_first()
        items['company_name'] = response.xpath(r"//div//a[@class='contentpile__content__wrapper__item__info__box__cname__title company_title']//text()").extract_first()
        items['city'] = response.xpath("//div//ul[@class='contentpile__content__wrapper__item__info__box__job__demand']/li[1]//text()").extract_first()
        items['experience'] = response.xpath("//div//ul[@class='contentpile__content__wrapper__item__info__box__job__demand']/li[2]//text()").extract_first()
        items['education'] = response.xpath("//div//ul[@class='contentpile__content__wrapper__item__info__box__job__demand']/li[3]//text()").extract_first()
        
        yield items


    # def parse(self,response):

    #     pass
    #     print("捉到我一次!")
    #     print(response)

    #     title = response.xpath("//title/text()").extract()
    #     title1 = response.xpath("//title/text()").extract_first()
    #     print(title)
    #     print(title1)

    #     #然后就可以写规则了.
        