import requests
import lxml
import re 
from multiprocessing import Pool
import json
from datetime import datetime



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




def crawler_zhilian():

    #处理页数问题
    #随机获得一个
    
    #城市代码
    city_code = '763'
    #每页获取得到的结果
    page_size = '100'

    #首先设定第一页获取所有的总页面的数量
    first_url = "https://fe-api.zhaopin.com/c/i/sou/?cityId=%s"%city_code

    res_html = requests.get(first_url)

    # print(len(decode_2_json(res_html)['data']['results']))
    #得出数量
    total = int(decode_2_json(res_html)['data']['numFound'])
    #计算总页数,四舍五入
    total_page = total // int(page_size)
    # print(total_page)

    #获取得到总页数之后,就可是循环了.!

    mutil_pool = Pool(4)

    for x in range(1,5):

        file_name = "zhilian_zhaopin_"+str(x)+'.json'
        url = "https://fe-api.zhaopin.com/c/i/sou/?cityId=%s&start=%s&pageSize=%s"%(city_code,int(page_size)*(x-1),page_size)
        print(url)
        mutil_pool.apply_async(decode_and_save_file,args=(url,file_name))
    
    mutil_pool.close()
    mutil_pool.join()
        
            

def decode_and_save_file(url,file_name):
    content = requests.get(url)
    content_dict = content.content.decode()
    # content_dict = decode_2_json(content)
    with open(file_name,'w') as file1:
        file1.write(content_dict)


if __name__ == "__main__":

    show_time()
    crawler_zhilian()
    show_time()