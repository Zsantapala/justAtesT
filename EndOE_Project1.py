#-*-coding:utf-8 -*-
#!/usr/bin/python
from bs4 import BeautifulSoup
import re,time,requests,os,threading

def save_img(img_arrd_list):
    for img in img_arrd_list:
        url='http:'+img
        pic=requests.get(url).content
        name = 'img//'+re.findall(r'\b\w+.jpg\b',img)[0]
        with open(name,'wb') as f:
            f.write(pic)

def open_web(start,end):
    print ('正在下载%d--%d的图片\n'%(start,end))
    for i in range(start,end+1):
        #创建线程锁避免主线程提前退出而出错
        lock = threading.Lock()
        lock.acquire()
        web='https://www.qiushibaike.com/imgrank/page/%d' %i
        get_w=requests.get(web).text
        soup=BeautifulSoup(get_w,'lxml')
        find_img=soup.find_all('img',attrs={"class":"illustration"})
        img_arrd_list=[x['src'] for x in find_img]
        #生成新的子线程来加快下载图片速度
        son_thread=threading.Thread(target=save_img,args=(img_arrd_list,))
        son_thread.start()
        #释放线程锁
        lock.release()

def qiushi_analy():
    print ('正在解析网址请稍后......')
    #打开网址并以文本方式显示
    get_web=requests.get('https://www.qiushibaike.com/imgrank/').text
    #创建BS对象解析HTML
    analysis_p=BeautifulSoup(get_web,'lxml')
    #解析网页列表Li标签推测与多少页
    page=analysis_p.find_all('ul',attrs={"class":"pagination"})[0].find_all('a',attrs={"rel":"nofollow"})
    last_page=int(re.findall(r'\d+',page[-2].span.string)[0])
    print ('搜索到网址共有%d页' %last_page)
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
        if start_num>13 or end_num>13:
            print ('本站最多只有%d页,请重新输入' %last_page)
            continue
        elif end_num<start_num:
            print ('你开玩笑的吧')
            new_num=end_num
            end_num=start_num
            start_num=end_num
            break
        else:
            break
    #创建多线程打开多页网址
    main_theard=threading.Thread(target=open_web,args=(start_num,end_num))
    main_theard.start()
    print ('图片下载成功......')

if __name__=='__main__':
    #判断文件夹是否存在
    if os.path.exists('img')==False:
        os.mkdir('img')
    qiushi_analy()
