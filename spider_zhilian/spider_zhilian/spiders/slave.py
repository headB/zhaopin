#尝试一下搞分布式,这个就是属于从客户端了.
import requests
from lxml import etree
import redis

#连接redis数据库

#定义好连接的redis主机
redis_info = {}
redis_info['host'] = '127.0.0.1'
redis_info['port'] = 6379
redis_info['password'] = ''

#返回一个redis连接类
conn_redis = redis.StrictRedis(host=redis_info['host'],port=redis_info['port'],password=redis_info['password'])

#尝试去redis中获取需要等待请求的url地址,并且,处理完一个就drop一个记录
#所以这里用到的方法自然就是pop


def search_and_request():
    #首先去尝试循环列出请求
    all_keys = conn_redis.keys()
    for x in all_keys:
        print(type(x))
    request_key = [str(x.decode()) for x in all_keys if str(x.decode()).startswith('request') ]
    #得到所有请求的关键key了
    #然后利用lpop
    
    #并且需要获取列表的长度
    for x in request_key:
        #因为是可能是并发执行请求,所以得上except机制,
        try:

            #一直尝试在redis获取某一个key里面的键值,如果为False的话,就下一个
            request_url = conn_redis.lpop(x).decode()
            while request_url:

                #然后就去请求,并且又保存到数据库当中.也是,以城市code为键值
                print(request_url)

                request_url = conn_redis.lpop(x).decode()

            #获取每一个key的长度
            # key_len = conn_redis.llen(x)
            # for x1 in range(int(key_len)+1):
            #     request_url = conn_redis.
            #     print(x1)
            #     #执行捉取任务,然后,执行完了之后就删除url请求
            #     pass
            #     conn_redis.
        except Exception as e:
            print(e)
            #然后继续下一个,不要停下来


search_and_request()