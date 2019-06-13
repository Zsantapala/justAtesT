#-*-conding:utf-8-*- 
import os,re,time

def catchfile(keyword,cwd):
	Scandir=os.walk(cwd)
	result_dir=[]
	result_file=[]
	result_inf=[]
	for abspath,childdirname,filename in Scandir:
		if childdirname:           #判断是否有子目录
			for d in childdirname:       #判断子目录名是否匹配
				if keyword in childdirname:
					result_dir.append(abspath+'\\'+childdirname)
		if filename:                   #判断文件列表是否存在
			for f in filename:
				file_abs=abspath+'\\'+f
				if keyword in f:
					result_file.append(file_abs)
				if re.search(r'\.txt',f):                     #只能判断txt文本文件
					try:                                      #只能解析非字节码编码文本文件
						with open(file_abs) as rf:
							for content in rf.readlines():
								if keyword in content:
									result_inf.append(file_abs)
					except UnicodeDecodeError:
						print ('无法解析此文本%s' %file_abs)
	total_re=result_dir+result_file
	r1=' '.join(total_re)
	r2=' '.join(result_inf)
	return (r1,r2)

if __name__=='__main__':
	while True:
		CWD=os.getcwd()
		print ('你当前的所在目录为%s' %CWD)
		changedir=input('是否查询当前目录下(可以输入指定目录，或回车继续)')
		if changedir:
			CWD=changedir
		elif changedir=='.':
			CWD=os.getcwd()
		elif changedir=='..':
			CWD=os.path.dirname(os.getcwd())
		keyw=input('输入关键字......\n')
		re1,re2=catchfile(keyw,CWD)
		print ('loading..........')
		time.sleep(5)
		print ('当前目录和子目录含有关键字的目录名和文件名为：%s' %(re1))
		print ('当前目录和子目录含有关键字内容的文件为（仅限txt文件）：%s' %(re2))
		contin=input('是否继续，继续直接，输入任意字符退出')
		if contin:
			break


