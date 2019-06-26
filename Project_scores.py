#-*-coding:utf-8-*-
#!/usr/bin/python
def score(s):
	if int(s)<60:
		return '不及格'
	else :
		return str(s)

# 读取文本直接运用列表生成式生成列表
with open('report.txt',encoding='utf-8') as f:
	report=[x.split() for x in f.readlines()]

#添加每位同学总成绩和平均成绩
for i in range(1,len(report)):
	report[i].append(sum(map(int,report[i][1:])))                             #运用map函数把每位同学每项成绩换成int类型的列表，再由sum函数算总分，最后添加到子列表(同学)中
	report[i].append(round(int(report[i][-1])/len(report[i][1:-1]),1))              #前面生成的总分与课程数相除得到平均分，round函数只保留小数点前面数字

#添加平均值
avg_value=['平均']
#添加每门课平均数
avg_value=avg_value+[round(sum(map(lambda x:int(x[avg]),report[1:]))/len(report[1:])) for avg in range(1,len(report[1])-1)]
#写的有点复杂，先用列表生成式提取文本列表的游标(index)值，再用lambda函数提取已avg为引索的int值，再由map生成每门成绩列表，然后由sum求和，再除以学生数，最后round去掉小数点	
avg_value.append(round(sum(avg_value[1:-1])/9,1))                             #总平均数

#修改report总列表
report.insert(1,avg_value)
report=report[:2]+sorted(report[2:],key=lambda x:x[-1],reverse=True)      #根据平均成绩排序

#新建空字符串，然后把列表内容依次写入
Fina_report=''
for ini in range(len(report)):
	if ini==0:
			report[ini].insert(0,'名次')
			report[ini].append('总分')
			report[ini].append('平均分')
			Fina_report='  '.join(report[ini])+'\n'
	elif ini==1:
		report[1].insert(0,'0')
		Fina_report+=report[1][0]+'   '+'   '.join(map(str,report[1][1:]))+'\n'
	else:
		report[ini].insert(0,str(ini-1))                                          #添加排序数
		#添加成绩，并用score函数判断是否低于60分，如果是则换成'不及格'字符串
		Fina_report+='   '.join(report[ini][:2])+'   '+'   '.join(map(score,report[ini][2:-2]))+'   '+'   '.join(map(str,report[ini][-2:]))+'\n'

#保存文档
with open('Final_report.txt','w',encoding='utf-8') as wf:
	wf.write(Fina_report)
