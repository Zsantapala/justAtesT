#-*-coding:utf-8-*-
#!/usr/bin/python
import requests
#引入的是https://www.tianqiapi.com/这个网站的API接口

def Weather():
    get_city=input('请输入你想要查询的城市\n')
    print ('正在查询请稍后......')
    get_weather=requests.get('https://www.tianqiapi.com/api/?version=v6&city=%s' %get_city)
    get_info=get_weather.json()
    #测试当输入错误的城市会返回默认城市的天气，只要输入的城市与获得的城市不符就判断错误
    if get_info["city"]==get_city:
        print ('%s今天的天气为%s,现在温度为%s摄氏度'%(get_info["city"],get_info["wea"],get_info["tem"]))
        print ('今天最低温度%s摄氏度,最高温度%s摄氏度' %(get_info["tem2"],get_info["tem1"]))
    else:
        print ('道歉没能查到你要的城市的天气')

while True:
    Weather()
    contin=input('输入out退出')
    if contin=='out':
        break