#-*-coding:utf-8-*-
#!/usr/bin/pthon
import os,time,xlwt  #pip install xlwt

def check_input(key,control=1):         #检查输入函数
	if control==1:
		while True:	
			keys=input(key)
			try:
				int(keys)
				return keys
			except ValueError:
				print ('输入错误！！！')
				continue
	else:
		keys=input(key).strip()
		return keys


def AddAcount(dataB,dataC):                 #记账函数
	comp=check_input('交易对象：',0)
	income=check_input('收入/万：')
	expand=check_input('支出/万：')
	receivab=check_input('应收账款/万:')
	pyment=check_input('应出账款/万：')
	dataTimeB=time.localtime()
	dayB=time.strftime('%Y{Y}%m{m}%d{d}',dataTimeB).format(Y='年',m='月',d='日')
	timeB=time.strftime('%H:%M:%S',dataTimeB)
	addDataC=[comp,income,expand,receivab,pyment,dayB,timeB]
	dataC.append(addDataC)
	dataB_Recent=dataB[-1]
	addDataB=acounting(dataB_Recent,addDataC)
	dataB.append(addDataB)
	print ('\n')
	print ('当前资产状况:')
	print ('最新资产: %s' %addDataB[1])
	print ('最新负责: %s' %addDataB[2])
	print ('最新净资产: %s' %addDataB[3])
	print ('\n')
	return (dataB,dataC)

def iniBalance(dataB):                    #初始化资产负债表
	totalAcoun=check_input('请输入总资产/W:')
	Liabili=check_input('请输入负债/W:')
	Netasset=str(int(totalAcoun)-int(Liabili))
	dataTimeA=time.localtime()
	dayA=time.strftime('%Y{Y}%m{m}%d{d}',dataTimeA).format(Y='年',m='月',d='日')
	timeA=time.strftime('%H:%M:%S',dataTimeA)
	newDataB=[dayA,totalAcoun,Liabili,Netasset,timeA]
	dataB.append(newDataB)
	return dataB

def saveFiles(dataB,dataC):                        #保存文件
	dataB_change=''
	dataC_change='' 
	for data in dataB:
		dataB_change+=data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+data[4]+'\n'
	for  data in dataC:
		dataC_change+=data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+data[4]+' '+data[5]+' '+data[6]+'\n'
	with open('BalanceSheet.txt','w',encoding='utf-8') as wbf:
		wbf.write(dataB_change)
	with open('cur_acount.txt','w',encoding='utf-8') as wca:
		wca.write(dataC_change)

def loadFiles():                          #加载文件
	try:
		with open('BalanceSheet.txt','r',encoding='utf-8') as rbf:
			dataB=[x.split() for x in rbf.readlines()]
		with open('cur_acount.txt','r',encoding='utf-8') as rca:
			dataC=[y.split() for y in rca.readlines()]
		return (dataB,dataC)
	except FileNotFoundError:
		dataB=[['结算日期','资产/W','负债/W','净资产/W','结算时间']]
		dataC=[['交易对象','收入/W','支出/W','应收账款/W','应出账款/W','交易日期','交易时间']]
		return (dataB,dataC)

def acounting(dataB_Recent,addDataC):                        #资产计算函数
	totalAcoun=int(dataB_Recent[1])
	Liabili=int(dataB_Recent[2])
	income=int(addDataC[1])
	expand=int(addDataC[2])
	receivab=int(addDataC[3])
	pyment=int(addDataC[4])
	R_totalAcoun=totalAcoun+income-expand                     #result结果
	R_Liabili=Liabili+pyment-receivab
	R_Netasset=R_totalAcoun-R_Liabili
	dataTimeC=time.localtime()
	dayC=time.strftime('%Y{Y}%m{m}%d{d}',dataTimeC).format(Y='年',m='月',d='日')
	timeC=time.strftime('%H:%M:%S',dataTimeC)
	addDataB=[dayC,str(R_totalAcoun),str(R_Liabili),str(R_Netasset),timeC]
	return (addDataB)

def MainInq(dataB,dataC):
	print ('查账模式\n')
	print ('1.查询最近十笔记录')
	print ('2.查询与某公司交易往来')
	print ('3.查询最近资产负债状况')
	your_inq=input('请选择服务')
	print ('')
	if your_inq=='1':
		inqRecenReco(dataC)
	elif your_inq=='2':
		inqCompany(dataC)
	elif your_inq=='3':
		inqBalance(dataB)
	else:
		print ('退出查询....返回.....')
		time.sleep(2)


def inqCompany(dataC):                       #查询公司记录
	if len(dataC)==1:
		print ('你没有任何与其他公司的记录，快去添加记录吧！')
		return
	else :
		comp=input('请输入要查询的公司名').strip()
		compRecord=[]
		for company in dataC[1:]:
			if company[0]==comp:
				compRecord.append(company)
		if compRecord:
			print ('与%s共有%d笔交易\n' %(comp,len(compRecord)))
			for record in compRecord:
				print ('交易时间：%s' %record[5])
				print ('收入：%s' %record[1])
				print ('支出：%s' %record[2])
				print ('应收账款：%s' %record[3])
				print ('应付账款：%s\n' %record[4])
				print ('')
				return
		else:
			print ('您没有没有与%s公司的记录......' %comp)
			return 	

def inqRecenReco(dataC):                      #查询最近十笔记录
	if len(dataC)==1:
		print ('你没有任何与其他公司的记录，快去添加记录吧！')
		return
	elif 1<len(dataC)<10:
		print ('当前你总共只有%d笔记录' %(len(dataC)-1))
		print ('交易对象 收入 支出 应收账款 应付账款 交易时间')
		for record in dataC[:0:-1]:
			print (record[0],record[1],record[2],record[3],record[4],record[5])
	else:
		print ('最近十笔交易记录')
		print ('交易对象 收入 支出 应收账款 应付账款 交易时间')
		for record in dataC[:-11:-1]:
			print (record[0],record[1],record[2],record[3],record[4],record[5])

def inqBalance(dataB):                         #查询最新资产负债表
	catch_dataB=dataB[-1]
	print ('最新资产： %s万' %catch_dataB[1])
	print ('最新负债： %s万' %catch_dataB[2])
	print ('最新净资产： %s万' %catch_dataB[3])
	print ('最后更新时间： %s' %catch_dataB[0])

def txt_excel(txt,name):                       #生成Excel
	style0=xlwt.easyxf('font: name 微软雅黑, bold on')
	style1=xlwt.easyxf('font: name 微软雅黑,')
	wb=xlwt.Workbook()
	ws=wb.add_sheet(name)
	for lines in range(len(txt)):
		for rows in range(len(txt[lines])):
			if lines==0:
				ws.write(lines,rows,txt[lines][rows],style0)
			else:
				ws.write(lines,rows,txt[lines][rows],style1)
	wb.save('%s.xls' %name)

if __name__=='__main__':
	DforB,DforC=loadFiles()
	if len(DforB)==1:
			print ('你的资产负载表没有记录，请先输入相关资料！')
			DforB=iniBalance(DforB)
			saveFiles(DforB,DforC)
	while True:
		DforB,DforC=loadFiles()
		print ('1.查帐;  2.记账;  3.生成Excel文本;  4.其他任意字符退出；')
		service=input('请选择服务:')
		print ('')
		print ('')
		if service=='1':
			MainInq(DforB,DforC)
			print ('')
		elif service=='2':
			DforB,DforC=AddAcount(DforB,DforC)
			print ('')
			saveFiles(DforB,DforC)
		elif service=='3':
			txt_excel(DforB,'资产-负债表')
			txt_excel(DforC,'流水账单')
			print ('正在到处请稍等......')
			time.sleep(2)
		else:
			print ('程序退出......')
			time.sleep(3)
			exit()
