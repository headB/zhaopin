#尝试一下搞分布式,这个就是属于从客户端了.
import requests
from lxml import etree
import redis

#连接redis数据库

#定义好连接的主机
redis_info = {}
redis_info['host'] = '127.0.0.1'
redis_info['port'] = 6379
redis_info['password'] = ''

#返回一个redis连接类
conn_redis = redis.StrictRedis(host=redis_info['host'],port=redis_info['port'],password=redis_info['password'])

#尝试去redis中获取需要等待请求的url地址,并且,处理完一个就drop一个记录
#所以这里用到的方法自然就是pop

