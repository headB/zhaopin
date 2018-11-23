import requests
from lxml import etree
import re 
from multiprocessing import Pool
import json
from datetime import datetime
import os
import redis

#定义好连接的redis主机
redis_info = {}
redis_info['host'] = '127.0.0.1'
redis_info['port'] = 6379
redis_info['password'] = ''

#返回一个redis连接类
conn_redis = redis.StrictRedis(host=redis_info['host'],port=redis_info['port'],password=redis_info['password'])



def show_time():
    time = datetime.now().strftime("%H:%M:%S")
    print(time)



def decode_2_json(response_content):

    try:
        res = json.loads(response_content.content.decode())
    except Exception as e:
        print(e)
        return False
    
    return res



#得到city_code,然后模拟请求,插入到redis中
def crawler_zhilian(city_code):

    #处理页数问题
    #随机获得一个
    
    #城市代码
    # city_code = '763'
    #每页获取得到的结果
    page_size = '100'

    #请求获取具体城市的所有职位的信息的URL
    request_url = "https://fe-api.zhaopin.com/c/i/sou/?cityId="

    #首先设定第一页获取所有的总页面的数量
    first_url = request_url+city_code

    res_html = requests.get(first_url)

    # print(len(decode_2_json(res_html)['data']['results']))
    #得出数量
    total = int(decode_2_json(res_html)['data']['numFound'])
    #计算总页数,四舍五入
    total_page = total // int(page_size)
    # print(total_page)

    #获取得到总页数之后,就可是循环了.!

    # mutil_pool = Pool(4)

    

    for x in range(1,total_page):

        file_name = "zhilian_zhaopin_"+str(x)+'.json'
        url = request_url+"%s&start=%s&pageSize=%s"%(city_code,int(page_size)*(x-1),page_size)

        conn_redis.rpush("request_"+city_code,url)
        #然后生成的链接,插入到redis,等待被其他分布式的爬虫爬取资料.
        #想想不是啦,还是以省份为界限.

        # mutil_pool.apply_async(decode_and_save_file,args=(url,file_name))
    print(city_code+" is OK")
    # mutil_pool.close()
    # mutil_pool.join()
        
            

def decode_and_save_file(url,file_name):
    content = requests.get(url)
    content_dict = content.content.decode()
    # content_dict = decode_2_json(content)
    with open(file_name,'w') as file1:
        file1.write(content_dict)


#返回所有省份对应的id信息

#返回列表,其中,x['hot_citys']为热门城市,x['province']为除了4个直辖市的所有中国省份信息
def return_province_info():

    
    #随便获取首页,然后爬取所有的省份id什么的!

    #关键是,如何设置一个缓存机制,哈哈,这个时候又想到了redis了,因为,这个看起来,比较简单.!可以保存进度

    #然后呢,就是,完成搜索之后,就自动提交自己当前的数据到redis上面去,以保存进度.这样子的想法.

    #关键就是,可以细分思想,用不同的函数实现就好,都写在同一个地方就不好了.!

    #想到了,就是,当前页数爬完了,就保存到redis中报告去.

    url = "https://sou.zhaopin.com/?jl=763"

    #利用正则也好,lxml也好,先分离出来先,然后呢,哈哈哈,保存到redis也是可以的啦.!哈哈哈.
    #想想redis什么好了,就是,临时操作什么都好,因为不用遵循mysql,需要先建立数据表,还得考虑字段类型,什么的,然后还得考虑不能用root用户的.
    #想想都麻烦.

    

    response = requests.get(url).content.decode()
    scripts = etree.HTML(response).xpath("//script")[-6]
    city_info_json = json.loads(scripts.text.replace("__INITIAL_STATE__=",''))
    city_info = city_info_json['basic']['dict']['location']['province']
    hot_city_info = city_info_json['basic']['dict']['location']['hotcitys']

    city_list = {}
    city_list['hot_citys'] = hot_city_info[1:]
    city_list['province'] = city_info

    return city_list

    #然后想办法合并,不了,我的意思是,直接删除热门城市里面包括的.

    #合并可能也不至于吧.就是需要单独设置4个直辖市

    


#根据给定的省份参数,去尝试创建文件夹,
def create_dir(province_cde):

    #默认就在当前位置创建文件夹了.
    #懒人一步到位的方法就是,直接使用 异常机制来捕获,就省的很多麻烦事啦,哈哈哈

    try:
        os.mkdir(province_cde)
    except Exception as e:
        print(e)
    

#这里的实现的具体的话,    

#单独设计一个函数,用于把爬取的城市信息保存到redis当中
#1.需要确定当前城市的所提供的最大职位数量
#2.需要确保url的唯一性
#3.顺序并不是那么重要

#得出结果,保存到列表,但是不同的城市是否需要单独处理,我想想,可以尝试一下
#因为可能涉及到优先级的问题

def set_cityinfo_2_redis():
    pass
    #获取热门城市的信息'

def save_provinceinfo_2_mysql():
    pass


if __name__ == "__main__":

    show_time()
    #获取热门城市的city_code
    for x in return_province_info()['hot_citys']:
        crawler_zhilian(str(x['code']))
    show_time()