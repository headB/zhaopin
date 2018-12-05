#尝试利用numpy导入数据先
import numpy as np
import pandas as pd
from  matplotlib import font_manager
from  matplotlib import pyplot as plt

city_dict = {'530': '北京', '538': '上海', '765': '深圳', '763': '广州', '531': '天津', '801': '成都', '653': '杭州', '736': '武汉', '600': '大连', '613': '长春', '635': '南京', '702': '济南', '703': '青岛', '639': '苏州', '599': '沈阳', '854': '西安', '719': '郑州', '749': '长沙', '551': '重庆', '622': '哈尔滨', '636': '无锡', '654': '宁波', '681': '福州', '682': '厦门', '565': '石家庄', '664': '合肥', '773': '惠州'}

data_test = pd.read_csv("zhilian_zhaopin.csv")
# print(len(data_test)
#现在当务之急,就是把这些数据分类,按城市分类,也就是,看看具体分类有哪些方法


#我现在比较想知道就是,每一个城市的平均工资是多少.

#OK!我先统计这里有多少个城市先.!


#先尝试一下换标题先
print(type(data_test))

print(data_test[:0])

# data_tes t.reindex(columns=['a','b','c','d','e','f'])
# data_test.columns = ['a','b','c','d','e','f','g','h']
print(data_test)



data_test.loc[100:110,['edu_level','work_exp','salary','city_code']]


# group_data = data_test.groupby('city_code')['job_name'].count().sort_values()
group_data = data_test.groupby('city_code').count()['job_name']
group_data1 = data_test.groupby('city_code')['job_name'].count()
# group_data = data_test.groupby('city_code').size()
# group_data = data_test.groupby('city_code').count().sort_values(by='job_name',ascending=False)

#group_data = data_test.groupby('city_code')

# print(group_data.index)

print(type(group_data))
# print(group_data[530])
# print(group_data.sort_values(ascending=False))
# for x in group_data.index:
#     print(x)
group_data.index = [city_dict[str(x)] for x in group_data.index ]
group_data.sort_values(ascending=False)


#添加对中文的支持
#全局支持
import matplotlib
# from  pylab import 
matplotlib.rcParams['font.family'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus']=False
matplotlib.rcParams['font.size']=15

#局部支持
font_setting = font_manager.FontProperties(fname="/Users/lizhixuan/project/msyh.ttc",size=20)
f1 = plt.figure(figsize=(20,10),dpi=80)
plt.plot([ x for x in job_sort_number.index ],[ y for y in job_sort_number.values ],)
# plt.plot([ y for y in job_sort_number.values ],)
plt.xlabel('中国内地城市',fontproperties=font_setting)
# plt.xticks([ x for x in job_sort_number.index ],[ x for x in job_sort_number.index ],rotation=90)
plt.ylabel('职位数量(个)',fontproperties=font_setting)
plt.title('各城市职位需求图',fontproperties=font_setting)

# plt.plot(range(1,55,2),[ x for x in job_sort_number.values ])
# plt.xticks(range(1,30))
plt.show()