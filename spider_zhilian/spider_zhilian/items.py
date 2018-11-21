# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    #1.具体的城市
    city = scrapy.Field()
    #2.职位名称
    job_name = scrapy.Field()
    #职位描述
    #job_descirption = scrapy.Field()
    #3.职位薪资
    salary = scrapy.Field()
    #4.学历要求
    education = scrapy.Field()
    #5.经验
    experience = scrapy.Field()
    #6.公司名字
    company_name = scrapy.Field()
    




