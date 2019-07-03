#-*-coding:utf-8-*-
#!/usr/bin/python
#'https://www.qiushibaike.com/imgrank/'
import requests,re,threading,os
from bs4 import BeautifulSoup

class CrawlWeb(object):
    def __init__(self,geturl='',page='',sign1='',sign2=''):
        self.url=geturl
        self.page=geturl+page
        self.sign1=sign1
        self.sign2=sign2

    def regula1(self,web1):
        return []
    def regula2(self,web2):
        return []

    def open_web(self):
        print('正在解析网址请稍后......')
        # 打开网址并以文本方式显示
        get_web = requests.get(self.url).text
        # 创建BS对象解析HTML
        ana_web = BeautifulSoup(get_web, 'lxml')
        number = self.regula1(ana_web)
        try:
            last_page = int(number)
        except ValueError:
            print('last_page ValueError')
            return
        return last_page

    def save_img(self,img_arrd_list):
        for img in img_arrd_list:
            url = 'http:' + img
            pic = requests.get(url).content
            name = 'img//' + re.findall(r'\b\w+.jpg\b|\b\w+.gif', img)[0]
            with open(name, 'wb') as f:
                f.write(pic)


    def save_address(self,start,end):
        if start==end:
            print ('正在下载第%d页的图片' %start)
        else:
            print ('正在下载第%d页--%d页的图片' %(start,end))
        for i in range(start,end+1):
            # 创建线程锁避免主线程提前退出而出错
            lock = threading.Lock()
            lock.acquire()
            web = (self.page + self.sign1 +'%d'+self.sign2) %i
            get_w = requests.get(web).text
            soup = BeautifulSoup(get_w, 'lxml')
            find_img = self.regula2(soup)
            if find_img:
                img_arrd_list = [x['src'] for x in find_img]
            else:
                print ('error....')
                return
            # 生成新的子线程来加快下载图片速度
            son_thread = threading.Thread(target=self.save_img, args=(img_arrd_list,))
            son_thread.start()
            # 释放线程锁
            lock.release()


class QiuShi(CrawlWeb):
    def regula1(self,web1):
        page = web1.find_all('ul', attrs={"class": "pagination"})[0].find_all('a', attrs={"rel": "nofollow"})
        self.regu1=re.findall(r'\d+', page[-2].span.string)[0]
        return self.regu1
    def regula2(self,web2):
        self.regu2 = web2.find_all('img', attrs={"class": "illustration"})
        return self.regu2

class JianDan(CrawlWeb):
    def regula1(self,web1):
        page=web1.find_all('span', attrs={"class":"current-comment-page"})[0]
        self.regu1=re.findall(r'\d',page.text)[0]
        return self.regu1
    def regula2(self,web2):
        self.regu2 = web2.find_all('img', attrs={"referrerpolicy": "no-referrer"})
        return self.regu2

def correct_input(max_n):
    while True:
        while True:
            start_p = input('请输入开始页')
            end_p = input('请输入结束页')
            try :
                start_num=int(start_p)
                end_num=int(end_p)
                break
            except ValueError:
                print('请输入小于等于%d的数字....' %last_page)
                continue
        if start_num>max_n or end_num>max_n:
            print ('本站最多只有%d页,请重新输入' %last_page)
            continue
        elif end_num<start_num:
            print ('你开玩笑的吧')
            new_num=end_num
            end_num=start_num
            start_num=end_num
            return (start_num,end_num)
        else:
            return (start_num,end_num)

if __name__=='__main__':
    if os.path.exists('img')==False:
        os.mkdir('img')
    #QS=QiuShi('https://www.qiushibaike.com/imgrank/' , 'page/')
    #tt = threading.Thread(target=QS.save_address,args=(1,1))
    #tt.start()
    #tt.join()
    while True:
        choose=input('请选择想要抓取的图片网站1.糗事热图 2.煎蛋无聊图 3.退出\n')
        if choose=='1':
            QS=QiuShi('https://www.qiushibaike.com/imgrank/' , 'page/')
            totalpage=QS.open_web()
            s1,e1=correct_input(totalpage)
            tt1 = threading.Thread(target=QS.save_address, args=(s1,e1))
            tt1.start()
            tt1.join()
        elif choose=='2':
            JD=JianDan('http://jandan.net/ooxx/','page','-','#comments')
            totalpage=JD.open_web()
            s2,e2=correct_input(totalpage)
            tt2 = threading.Thread(target=JD.save_address, args=(s2,e2))
            tt2.start()
            tt2.join()
        else:
            print ('程序退出')
            break