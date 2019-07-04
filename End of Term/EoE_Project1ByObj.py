#-*-coding:utf-8-*-
#!/usr/bin/python
#'https://www.qiushibaike.com/imgrank/'
import requests,re,threading,os
from bs4 import BeautifulSoup

#父类抓取网页
class CrawlWeb(object):
    #初始化
    def __init__(self,geturl='',page='',sign1='',sign2=''):
        self.url=geturl
        self.page=geturl+page
        self.sign1=sign1
        self.sign2=sign2

    #两个规则留给子类各自定义
    def regula1(self,web1):
        return []
    def regula2(self,web2):
        return []

    #解析热图网址有几页并返回页数
    def open_web(self):
        print('正在解析网址请稍后......')
        # 打开网址并以文本方式显示
        get_web = requests.get(self.url).text
        # 创建BS对象解析HTML
        ana_web = BeautifulSoup(get_web, 'lxml')
        number = self.regula1(ana_web)
        if number:
            try:
                last_page = int(number)
            except ValueError:
                print('last_page ValueError')
                return
        return last_page

   #从save_address得到图片地址列表分别打开并保存图片
    def save_img(self,img_arrd_list):
        try:
            for img in img_arrd_list:
                print ('开始下载%s' %img)
                url = 'http:' + img
                pic = requests.get(url).content
                name = 'img//' + re.findall(r'\b\w+.jpg\b|\b\w+.gif', img)[0]
                with open(name, 'wb') as f:
                    f.write(pic)
                print ('下载结束')
        except :
            print ('save_img()Error')


    def save_address(self,start,end):
        if start==end:
            print ('正在下载第%d页的图片' %start)
        else:
            print ('正在下载第%d页--%d页的图片' %(start,end))
        for i in range(start,end+1):
            print ('下载第%d页图片' % i)
            web = (self.page + self.sign1 +'%d'+self.sign2) %i
            try:
                get_w = requests.get(web).text
            except :
                print ('save_address() get_w error')
            soup = BeautifulSoup(get_w, 'lxml')
            find_img = self.regula2(soup)
            if find_img:
                img_arrd_list = [x['src'] for x in find_img]
            else:
                print ('can\'t get data in %s' % web)
                return
            # 生成新的子线程来加快下载图片速度
            son_thread = threading.Thread(target=self.save_img, args=(img_arrd_list,))
            son_thread.start()
            son_thread.join()
            print ('第%d页下载结束' % i)

class QiuShi(CrawlWeb):
    #自定义Qiushi的规则
    def regula1(self,web1):
        page = web1.find_all('ul', attrs={"class": "pagination"})[0].find_all('a', attrs={"rel": "nofollow"})
        self.regu1=re.findall(r'\d+', page[-2].span.string)[0]
        return self.regu1
    def regula2(self,web2):
        self.regu2 = web2.find_all('img', attrs={"class": "illustration"})
        return self.regu2

class JianDan(CrawlWeb):
    # 自定义JianDan的规则
    def regula1(self,web1):
        page = web1.find_all('span', attrs={"class":"current-comment-page"})[0]
        self.regu1 = re.findall(r'\d',page.text)[0]
        return self.regu1
    def regula2(self,web2):
        self.regu2 = web2.find_all('img', attrs={"referrerpolicy": "no-referrer"})
        return self.regu2

#输入页数判断函数
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
                print('请输入小于等于%d的数字....' %max_n)
                continue
        if start_num>max_n or end_num>max_n:
            print ('本站最多只有%d页,请重新输入' %max_n)
            continue
        elif end_num<start_num:
            print ('你开玩笑的吧。。。。')
            new_num=end_num
            end_num=start_num
            start_num=end_num
            return (start_num,end_num)
        else:
            return (start_num,end_num)

if __name__=='__main__':
    if os.path.exists('img')==False:
        os.mkdir('img')
    while True:
        choose=input('请选择想要抓取的图片网站1.糗事热图 2.煎蛋无聊图 3.退出\n').strip()
        if choose=='1':
            QS=QiuShi('https://www.qiushibaike.com/imgrank/' , 'page/')
            totalpage = QS.open_web()
            print ('本站热图总共有%d页' %totalpage)
            s1,e1=correct_input(totalpage)
            tt1 = threading.Thread(target=QS.save_address, args=(s1,e1))
            tt1.start()
            tt1.join()
        elif choose=='2':
            JD=JianDan('http://jandan.net/ooxx/','page','-','#comments')
            totalpage = JD.open_web()
            print ('本站无聊图一共有%d页' %totalpage)
            s2,e2 = correct_input(totalpage)
            tt2 = threading.Thread(target=JD.save_address, args=(s2,e2))
            tt2.start()
            tt2.join()
        else:
            print ('程序退出')
            break