#-*-coding:utf-8-*-
#!/usr/bin/python
import re,time

#读取文件
with open('from.txt','r',encoding='utf-8') as f:
    content=f.read()

#设置规则
match_Words=re.compile(r'\b[A-z]+\b')
#匹配并生成列表
result=re.findall(match_Words,content)
#排序列表--忽略大小写
result=sorted(result,key=lambda x:x.lower(),)
print (result)
#保存文件
with open('to.txt','w',encoding='utf-8') as txt:
    #.join方法
    txt.write('\n'.join(result))

