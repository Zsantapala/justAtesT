#-*-coding:utf-8-*-
#!/usr/bin/python
import requests
#引入的是https://www.tianqiapi.com/这个网站的API接口
get_city=input('请输入你想要查询的城市\n')
print ('正在查询请稍后......')
get_weather=requests.get('https://www.tianqiapi.com/api/?version=v6&city=%s' %get_city)
get_info=get_weather.json()
if get_info["city"]==get_city:
    print ('%s今天的天气为%s,现在温度为%s摄氏度'%(get_info["city"],get_info["wea"],get_info["tem"]))
else:
    print ('道歉没能查到你要得城市天气')