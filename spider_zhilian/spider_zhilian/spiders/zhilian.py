#写一个爬虫尝试爬取智联招聘

from scrapy.spiders import Spider,CrawlSpider
#添加去重
# from scrapy.dupefilters import RFPDupeFilter
#添加Rule,用于,匹配大量的网址
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

#导入item类
from spider_zhilian.items import SpiderZhilianItem



#就是,爬虫教程,有提及的,就是,最基本的爬虫,包括了
#item
#name
#start_urls
#parse(这个是后续的处理吧)

def request_url_organize():

    url_dict = {
        'start':60,
'pageSize':60,
'cityId':763,
'areaId':'',
'businessarea':"{}",
'industry':'',
'salary':'',
'workExperience':-1,
'education':-1,
'companyType':-1,
'employmentType':-1,
'jobWelfareTag':-1,
'jobType':-1,
'sortType':'',
'kw':'',
'kt':'3',
'bj':'',
'sj':'',
'lastUrlQuery':'%7B%22p%22:2,%22jl%22:%22763%22%7D',
'companyNo':'',
'companyName':'',
'_v':0.27099139,
'x-zp-page-request-id':'0d5491a7231542678eb12bcb4109a6df-1542783251118-640775'
    }
    return url_dict



class zhiLianSpider(CrawlSpider):
    name = "zhilian_1"
    allowed_domains = ['zhaopin.com']
    start_urls = [
        'https://sou.zhaopin.com/?jl=489',
    ]
    
    rules = (
        Rule(LinkExtractor(allow=("xx")),callback='process_job_info',follow=True),
        Rule(LinkExtractor(allow=(r"https://sou.zhaopin.com/\?jl=489$")),callback='process_job_info',follow=True)
        ,
    )


    def process_job_info(self,response):
        # pass
        #尝试每一个结果,提取里面的关键字,例如是,职位,公司名称,薪资.
        print(request_url_organize())
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
        