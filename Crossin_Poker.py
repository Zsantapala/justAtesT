# -*- conding:utf-8 -*-
from random import *

def Poker():
	List1=['♥','♠','♣','♦']
	List2=[str(x) for x in range(2,11)]+['A','J','Q','K']
	Poker=[]
	for i in List1:
		for j in List2:
			Poker.append(i+j)
	Poker.append('Red Joker')
	Poker.append('Black Joker')
	return Poker

def ShuffleCard(n,poker):
	p1=[]
	p2=[]
	p3=[]
	d=[]
	m=0
	for Shuffle in range(n):   #洗牌
		shuffle(poker)
	random_d=sample(list(range(54)),3) #随机发底牌
	random_d.sort()
	while m<54:
		if m in random_d:
			d.append(poker[m])
			m+=1
		elif m<54:
			p1.append(poker[m])
			m+=1
		if m in random_d:
			d.append(poker[m])
			m+=1
		elif m<54:
			p2.append(poker[m])
			m+=1
		if m in random_d:
			d.append(poker[m])
			m+=1
		elif m<54:
			p3.append(poker[m])
			m+=1
		else:
			continue
	return (p1,p2,p3,d)

def play():
	player1=input('请输入选手1的名字')
	player2=input('请输入选手2的名字')
	player3=input('请输入选手3的名字')
	times=int(input('请输入洗牌的次数'))
	Cpoker=Poker()
	P1_re,P2_re,P3_re,Dipai=ShuffleCard(times,Cpoker)
	print (player1+'手牌是'+' '.join(P1_re)+'\n')
	print (player2+'手牌是'+' '.join(P2_re)+'\n')
	print (player3+'手牌是'+' '.join(P3_re)+'\n')
	print ('底牌是'+' '.join(Dipai))

if __name__=='__main__':
	play()