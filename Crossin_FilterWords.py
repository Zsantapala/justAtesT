#-*coding:utf-8-*-
import pickle,time,jieba

def Add_words(Word):
	Words=check_file()
	time.sleep(3)
	with open('Fliter.txt','wb') as f:
		Words.append(Word.strip().lower())
		pickle.dump(Words,f)
		print ('正在保存文件请稍后......')
		time.sleep(3)

def check_file():
	try:
		with open('Fliter.txt','rb') as rf:
			Get_list=pickle.load(rf)
			return Get_list
	except FileNotFoundError:
		print ('没有文件，正在创建文件请稍后.....')
		time.sleep(2)
		with open('Fliter.txt','wb') as cf:
			ini_Files=[]
			pickle.dump(ini_Files,cf)
			return ini_Files


def FliterW(Inputw):
	Fenci=[x for x in jieba.cut(Inputw)]
	for F in Fenci:
		changeF=mainFliter(F.lower())
		if changeF:
			Fenci[Fenci.index(F)]=changeF
	result=''.join(Fenci)
	return result

def mainFliter(String):
	Words=check_file()
	for w in Words:
		String=String.replace(w,'*'*len(w))
	return String


if __name__=='__main__':
    print ('欢迎进入屏蔽词程序，正在检查文件请稍后......')
    Check=check_file()
    if Check==[]:
    	print ('你还未输入屏蔽词')
    	input_w=input('请输入屏蔽词\n')
    	Add_words(input_w)
    	get_string=input('请输入一段文字\n')
    	print (FliterW(get_string))
    print ('输入FliterW(\'任意一段文字\')给出屏蔽结果')
    print ('输入Add_words(\'屏蔽词\')添加屏词')


