#-*-coding:utf-8-*-
#!/usr/bin/python
#'https://www.qiushibaike.com/imgrank/'
import requests,re,threading,os
from bs4 import BeautifulSoup
class CrawlWeb(object):
    def __init__(self,geturl='',page=''):
        self.url=geturl
        self.page=geturl+page

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
        page = self.regula1(ana_web)
        last_page = int(re.findall(r'\d+', page[-2].span.string)[0])
        return last_page

    def save_img(self,img_arrd_list):
        for img in img_arrd_list:
            url = 'http:' + img
            pic = requests.get(url).content
            name = 'img//' + re.findall(r'\b\w+.jpg\b', img)[0]
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
            web = self.page+'%d' %i
            get_w = requests.get(web).text
            self.soup = BeautifulSoup(get_w, 'lxml')
            self.find_img = self.regula2(self.soup)
            if self.find_img:
                img_arrd_list = [x['src'] for x in self.find_img]
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
        self.regu1 = web1.find_all('ul', attrs={"class": "pagination"})[0].find_all('a', attrs={"rel": "nofollow"})
        return self.regu1
    def regula2(self,web2):
        self.regu2 = web2.find_all('img', attrs={"class": "illustration"})
        return self.regu2

class JianDan(CrawlWeb):
    def regula1(self,web1):
        page=web1.find_all('span', attrs={"class":"current-comment-page"})[0]
        self.regu1=re.findall(r'/d',page).[0]
        return self.regu1
    def regula2(self,web2):
        self.regu2 = web2.find_all('img', attrs={"referrerpolicy": "no-referrer"})
        return self.regu2


if __name__=='__main__':
    if os.path.exists('img')==False:
        os.mkdir('img')
    QS=QiuShi('https://www.qiushibaike.com/imgrank/' , 'page/')
    tt = threading.Thread(target=QS.save_address,args=(1,2))
    tt.start()