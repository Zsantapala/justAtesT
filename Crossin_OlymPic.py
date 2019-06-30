#-*- coding:utf-8 -*-
#!/usr/bin/python
class Nation(object):
    def __init__(self,na,go,sl,br):
        self.nation=na
        self.gold=go
        self.sliver=sl
        self.bronze=br
    def get_Medal(self,n_go,n_sl,n_br):
        self.gold+=n_go
        self.sliver+=n_sl
        self.bronze+=n_br

    @property
    def count_total(self):
        return self.gold+self.sliver+self.bronze

    def __str__(self):
        return '{0}: Gold {1},Sliver {2},Bronze {3} '.format(self.nation,self.gold,self.sliver,self.bronze)

def medal_List(m_list,sort_meth='gold'):
    if sort_meth=='gold':
        Ord_Gold=sorted(m_list,key=lambda x:x.gold,reverse=True)
        for i in range(len(Ord_Gold)):
            print ('金牌数排行榜：\n')
            print ('No.%d:'%(i+1),Ord_Gold[i])
    else:
        Ord_Total=sorted(m_list,key=lambda x:x.count_total,reverse=True)
        for j in range(len(Ord_Total)):
            print ('奖牌总数排行榜：\n')
            print ('No.%d:'%(j+1),Ord_Total[j] )

if __name__=='__main__':
    CHN=Nation('中国',26,18,26)
    US=Nation('美国',46,37,38)
    UK=Nation('英国',27,23,17)
    print (CHN)
    print (US)
    print (UK)
    print ('中国新增了一些奖牌！！')
    CHN.get_Medal(3,2,1)
    print (CHN)
    Medal_list=[CHN,US,UK]
    medal_List(Medal_list)
    medal_List(Medal_list,'total')