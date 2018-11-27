#尝试一下搞分布式,这个就是属于从客户端了.
import requests
from lxml import etree
import redis
from multiprocessing import Pool
from .multi_spider import conn_redis

#连接redis数据库

#定义一个用户连接数据库的函数

#定义好连接的redis主机
# redis_info = {}
# redis_info['host'] = '127.0.0.1'
# redis_info['port'] = 6379
# redis_info['password'] = ''

#设置一个全局变量,用于设置lpop方式获取和取消该数值
start_urls_exist = True

# def manu_conn_redis(redis_info):
#     return redis.StrictRedis(host=redis_info['host'],port=redis_info['port'],password=redis_info['password'])

# manu_conn_redis1 = manu_conn_redis(redis_info)
manu_conn_redis1 = conn_redis


#返回一个redis连接类
# conn_redis = redis.StrictRedis(host=redis_info['host'],port=redis_info['port'],password=redis_info['password'])

#尝试去redis中获取需要等待请求的url地址,并且,处理完一个就drop一个记录
#所以这里用到的方法自然就是pop

#因为多进程的时候,对方必须是函数,也不能是实例,所以,我这里,就封装一下那个爬取的函数啦.!
def request_2_redis(city_code):

    try:
        request_url = conn_redis.lpop(city_code).decode()
        print(request_url)
        #测试
        import time
        

        res = requests.get(request_url).content.decode()
        conn_redis.rpush("res_"+str(city_code),res)
    except Exception as e:
        return False
    
    return True


# def yield_res(x):
#     try:
#         res =  conn_redis.lpop(x).decode()
#         while res:
#             yield res
#             res = conn_redis.lpop(x).decode()
#     except Exception as e:
#         print(e)
#         yield False



def search_and_request():
    #首先去尝试循环列出请求
    all_keys = conn_redis.keys()
    request_key = [str(x.decode()) for x in all_keys if str(x.decode()).startswith('request')]

    # return request_key
    #得到所有请求的关键key了
    #然后利用lpop
    
    #并且需要获取列表的长度

    #然后这里需要用到多进程技术,然后这里采用的就是进程池了,因为,简单,也是比较实用,而且处理速度的确都是快
    pool = Pool(4)
    
    for x in request_key:
    #     #因为是可能是并发执行请求,所以得上except机制,
        
        
        try:

            #度量当前x的长度,然后就是循环多少次
            x_length= conn_redis.llen(x)
            # request_url.append(conn_redis.lpop(x).decode())
            for xx1 in range(x_length+1):
                # request_url = conn_redis.lpop(x).decode()
    #             #然后就去请求,并且又保存到数据库当中.也是,以城市code为键值
                # pool.apply_async(request_2_redis,args=(x,request_url))
                pool.apply_async(request_2_redis,args=(x,))
                
                # request_url = conn_redis.lpop(x).decode()

            
        except Exception as e:

            print(e)
            #然后继续下一个,不要停下来
        
        print(str(x)+" is OK ! ")
    pool.close()
    pool.join()


search_and_request()

#在这个时候,我想用递归了

# def check_start_urls():

#     #判断条件,然后继续递归自己
#     if not res:
#         return False

#     if xx:
#         check_start_urls()
#     else:
#         pass

if __name__ == "__main__":
    pass