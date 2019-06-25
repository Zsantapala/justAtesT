#-*-coding:utf-8--
#!/usr/bin/python
from random import randint
import pickle,time

game_Info=[]
def open_and_checkFile():   #打开并检查文件
	try:
		with open('GuessNum.txt','rb') as readf:
			global game_Info
			game_Info=pickle.load(readf)
	except FileNotFoundError:
		SaveFile()

def SaveFile():        #保存文件
	global game_Info
	with open('GuessNum.txt','wb') as writef:
		pickle.dump(game_Info,writef)

def getUser(inpuName):
	global game_Info
	if game_Info:
		for name in game_Info:
			if name[0]==inpuName:
				print ('欢迎回来%s' %(inpuName))
				return name
		else:
			print('欢迎新玩家！！%s' %inpuName)
			return [inpuName,0,0,0]
	else :
		print ('欢迎新玩家！！%s' %(inpuName))
		return [inpuName,0,0,0]
def saveRecord(userecord):
	global game_Info
	if game_Info:
		for user in game_Info:
			if user[0]==userecord[0]:
				game_Info[game_Info.index(user)]=userecord
			else:
				game_Info.append(userecord)
	else:
		game_Info.append(userecord)

def MainGame():
	open_and_checkFile()
	Your_name=input('请输入你的用户名.....').lower()
	userinfo=getUser(Your_name)
	print ('游戏现在开始......')
	total_count=userinfo[1]
	total=userinfo[2]
	while True:
		count=1
		num=randint(1,100)
		while True:
			while True:
				try:
					your_guess=int(input('请输入你要猜的1-100之间的整数：'))
					if your_guess in range(1,100):
						break
				except ValueError:
					print ('输入错误！！')
					continue
			print ('本轮第%s次' %count)
			if your_guess<num :
				print ('可惜，你猜小了！')
			elif your_guess>num:
				print ('可惜，你猜大了！')
			else:
				print ('恭喜你！！猜中了！正确数字就是%d' %num)
				break
			count+=1	
		total+=count
		print (count)
		if userinfo[3]==0:
			userinfo[3]=count
		else:
			userinfo[3]=min(userinfo[3],count)
		total_count+=1
		Y_continue=input('还要再来一局吗？（按q或Q退出游戏.....）')
		if Y_continue=='q' or Y_continue=='Q':
			userinfo[1]=total_count
			userinfo[2]=total
			saveRecord(userinfo)
			if total_count==0:
				avg=0
			else:
				avg=float(total)/float(total_count)
			print ('你一共玩了%d局，其中最好成绩是%d次猜对，平均每局%.2f次猜对' %(total_count,userinfo[3],avg))
			time.sleep(5)
			SaveFile()
			break
		
if __name__=='__main__':
	MainGame()
