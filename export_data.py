import csv
import json

from spider_zhilian.spider_zhilian.spiders.multi_spider import conn_redis
#尝试将redis数据库当中的数据导出为csv格式

#哈哈.这个时候,又得使用生成器了,

def read_data_from_redis():
    #先读取所有的key
    keys_info = conn_redis.keys()
    
    #然后就是利用生成器,返回数据
    for x in keys_info:
        if x.decode().startswith("res"):
            try:
                x = x.decode()
                print(x)
                content = []
                content_len = conn_redis.llen(x)
                print("这个res的结果有: %s 条"%content_len)

                for x1 in range(content_len-1):
                    # content_json = 
                    content_res = conn_redis.lindex(x,x1)
                    yield json.loads(content_res.decode())
            except Exception as e:
                print(e)


def handle_json_data_zhilian_2_list(json_datas):
     
     #必须是按顺序,导出智联招聘的字段信息,然后输出为list

    for json_data in json_datas:

        try:
            for x in json_data['data']['results']:
                list_all = []
                list1 = []
                #职位名称
                list1.append(x['jobName'])
                #地点
                list1.append(x['city']['display'])
                #工作经验
                list1.append(x['workingExp']['name'])
                #学历
                list1.append(x['eduLevel']['name'])
                #薪资
                list1.append(x['salary'])
                #公司名字
                list1.append(x['company']['name'])
                #公司福利
                list1.append(",".join(x['welfare']))
                #区域代码
                list1.append(x['city']['items'][0]['code'])

                list_all.append(list1)

                yield list_all
        except Exception as e:
            print(e)
            



#然后可以写入数据
def write_2_file(data):

    with open('zhilian_zhaopin.csv','w',newline='') as file1:
        try:
            writer = csv.writer(file1)
            for x in data:
                for x1 in x:
                    writer.writerow(x1)
        except Exception as e:
            print(e)
            print()


#返回结果生成器
res = read_data_from_redis()

#返回格式化后的生成器
data = handle_json_data_zhilian_2_list(res)

print("I am kumanxuan!")

#然后调用函数去写入数据了
write_2_file(data)