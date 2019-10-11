#-*-coding:utf-8-*-
#!/usr/bin/python
import requests, re, threading, os
from bs4 import BeautifulSoup

class JianDan:
    # 初始化
    def __init__(self, geturl=''):
        self.url = geturl
        self.next_page = ''

    def regula1(self, web1):
        self.regu2 = web1.find_all('img', attrs={"referrerpolicy": "no-referrer"})
        return self.regu2
    def open_page(self, web):
        next_page = web.find_all('a', attrs={"class": "previous-comment-page"})[0]
        if next_page:
            self.next_page = 'http:' + next_page['href']
            return True
        else:
            return False

    def save_img(self, img):
        try:
            print('开始下载%s' % img)
            url = 'http:' + img
            pic = requests.get(url).content
            name = 'img//' + re.findall(r'\b\w+.jpg\b|\b\w+.gif', img)[0]
            with open(name, 'wb') as f:
                f.write(pic)
            print('%s下载结束' % img)
        except :
            print('save_img()Error')

    def open_address(self):
        try:
            goto = True
            while goto:
                if self.next_page == '':
                    web = self.url
                else:
                    web = self.next_page
                get_w = requests.get(web).text
                soup = BeautifulSoup(get_w, 'lxml')
                find_img = self.regula1(soup)
                goto = self.open_page(soup)
                if find_img:
                    img_arrd_list = [x['src'] for x in find_img]
                else:
                    print('can\'t get data in %s' % web)
                    return
                # 生成新的子线程来加快下载图片速度
                son_img = []
                for img in range(len(img_arrd_list)):
                    son_thread = threading.Thread(target=self.save_img, args=(img_arrd_list[img],))
                    # 开始运行多线程
                    son_thread.start()
                    # 把线程对象加入列表
                    son_img.append(son_thread)
                # 并发阻塞直到线程完毕
                for son_thread in son_img:
                    son_thread.join()


        except:
            print('save_address() get_w error')

if __name__ == '__main__':
    if os.path.exists('img') == False:
        os.mkdir('img')
    JD = JianDan('http://www.jandan.net/ooxx/')
    print('正在下载请稍等.......')
    JD.open_address()