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
job_sort_number = group_data.sort_values(ascending=False)
job_sort_number


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



#先单独设置y轴的取值范围
#其实感觉取了最大值,应该就差不多了吧.
#先计算出总的需要填充y轴的总的列表吧.


high_values = [x for x in job_sort_number.values]
label_list = [x for x in job_sort_number.index]
x_axis = range(0,len(label_list)*10,10)
max_values = max(high_values) + 50000
#设置范围,Y轴显示范围
leng1 = plt.figure(figsize=(30,14),dpi=80)
plt.ylim(2000,max_values)
# plt.yticks([x for x in range(0,max(high_values),50000)])
#设置Y轴标题
plt.ylabel("职位数量/个")
#然后开始尝试填充条形图,每一个值的Y值,纵轴
per_city = plt.bar(x_axis,high_values,width=9)
# plt.grid()#开启横向和纵向网格
plt.grid(axis='y')
#然后就尝试改变刻度了,让刻度显示索引
for x in per_city:
    plt.text(x.get_x()+2,x.get_height()+10000,str(x.get_height()//10000)+"万")
plt.xticks(x_axis,label_list)
plt.title("中国大陆地区,智联招聘中27个热门城市的职位需求数量(11月)")
plt.show()



#=========================================================================
#尝试去分析这个27个热门城市的所有职业的平均薪资


#这里感觉就需要处理薪资的特殊数据了,要整理了.

#ok,先分组,把jobname,salary,city_code拉出来


ava_salary_origin = data_test.loc[:,['city_code','job_name','salary']]

#尝试使用apply来应用特殊的数据处理了.
def let_K_2_number(data):
    
    import re
    import numpy as np
    
    salary_match = np.NAN
    
    try:
        splits = data.split("-")
        
        salary_match = int(re.findall('(\d+)K',splits[-1])[0])
        salary_match *= 1000
        
    except Exception as e:
        print(splits)
        print(e)
        
    return salary_match

ava_salary_origin['salary'] = ava_salary_origin['salary'].apply(let_K_2_number)

#判断是否存在空数据,错误数据
# print(ava_salary_origin.isnull())
#判断是否存在空数据,如果是,就抛弃整行数据
ava_salary_origin = ava_salary_origin.dropna()

print(ava_salary_origin)

#=========================================================================


#=======================分组统计数据,然后得到平均薪资==========================
#OK!开始处理

#分组数据
per_city_salary_data = ava_salary_origin.groupby("city_code")['salary'].mean().sort_values(ascending=False)
per_city_salary_data.index = [ city_dict[str(x)] for x in per_city_salary_data.index]
print(per_city_salary_data)

#===============================================================================


#===================统计平均薪资============================================================
#然后利用matplotlib画图


#条形图  bar图


#首先设置图像的大小
p1 = plt.figure(figsize=(20,10),dpi=80)





#y轴范围
#效果不怎么理想,切换手动刻度
# plt.ylim(0,12000)
plt.yticks([x for x in range(0,14000,1000)])


#得出需要展示多少个结果先
city_all_values = len(per_city_salary_data.index)

#然后还得设置x轴的,画图的起始坐标,是每一个
axis_list = range(city_all_values)

#对的,然后下面X轴显示的字段,要设置了.

axis_x_labels = [x for x in per_city_salary_data.index]
#x轴字段
#对x轴坐标相当敏感
plt.xticks(axis_list,axis_x_labels)


#y轴结果集
axis_y_values = [x for x in per_city_salary_data.values]


plt.title("智联招聘27个热门城市全部招聘岗位的平均薪资")
plt.ylabel("人民币(元)")

#然后就可以填充条形图了
plt.bar(axis_list,axis_y_values)
plt.grid(axis='y')

plt.show()
