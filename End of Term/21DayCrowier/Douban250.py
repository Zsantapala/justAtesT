#-*-coding:utf:8-*-
import requests, csv, threading, time, os, re
Moive = []
headers = ['Rnk', 'id', 'average', 'title', 'casts', 'Moive_url', 'image']

def getMoive(data, rnk):    #获取电影信息
    global Movie
    try:
        M_info = {
            'Rnk': rnk,
            'id': data['id'],
            'average':data['rating']['average'],
            'title': data['title'],
            'casts': ','.join(c['name'] for c in data['casts']),
            'Moive_url': 'https://api.douban.com/v2/movie/{id}?apikey=0df993c66c0c636e29ecbb5344252a4a'.format(id=data['id']),
            'image': data['images']['small'],
        }
        Moive.append(M_info)
    except:
        print('getMovie Error')

def openUrl(num):             #打开网页获取网页信息并调用getMoive获取电影信息
    url = 'https://api.douban.com/v2/movie/top250?start={num}&apikey=0df993c66c0c636e29ecbb5344252a4a'.format(num=str(num))
    try:
        page_data = requests.get(url).json()
        get_data = page_data['subjects']
        open_ts = []
        for m in range(len(get_data)):
            print('正在获取movie...... %d' %(m+1))
            rnk = num+m+1
            open_t = threading.Thread(target=getMoive, args=(get_data[m], rnk))
            open_t.start()
            open_ts.append(open_t)
        for t in open_ts:
            t.join()
    except:
        print('openUrl Error,please check code!')

def capAll():              #调用openurl函数打开所有相关网页
    ts1 = []
    for startnum in range(0, 250, 20):
        print('正在打开第%d个' %startnum)
        t1 = threading.Thread(target=openUrl, args=(startnum,))
        t1.start()
        ts1.append(t1)
    for t in ts1:
        t.join()

def save_as_csv(header,rows):   #保存csv文件
    try:
        with open('Movie250.csv', 'w', newline='') as f:
            f_csv = csv.DictWriter(f, header)
            f_csv.writeheader()
            f_csv.writerows(rows)
    except:
        print('saveError')

def read_from_csv():          #读取csv文件
    try:
        new_data = []
        with open('Movie250.csv', newline='') as r_csv:
            meta_data = csv.DictReader(r_csv)
            for d in meta_data:
                new_data.append(d)
            return new_data
    except FileNotFoundError:
        print('文件不存在')

def downloadIMG(moive):     #下载电影图片
    try:
        picurl = moive['image']
        picname = 'img//' + moive['title']+'.jpeg'
        get_pic = requests.get(picurl).content
        with open(picname, 'wb') as img:
            img.write(get_pic)
    except:
        print('downloadImg Error')
def get_all_img(data):    #批量下载电影图片
    tm_s = []
    for img in range(len(data)):
        tm = threading.Thread(target=downloadIMG, args=(data[img],))
        tm.start()
        tm_s.append(tm)
    for t in tm_s:
        t.join()

def display_info(movie):   #打印电影信息到控制台
    print('影片：'+movie['title'])
    print('排名第：'+movie['Rnk'])
    print('演员：'+movie['casts'])
    print('评分：'+movie['average'])

def int_or_str(key,data):    #判断输入
    try:
        num = int(key)
        for Rnk in data:
            if num == int(Rnk['Rnk']):
                return Rnk
    except ValueError:
        for title in data:
            if key == title['title']:
                return title

def get_input(info,data):    #分析输入数字
    catch_info = re.findall(r'\b\d-\w+|\b\d-\d+', info)
    if catch_info:
        g_info = catch_info[0].split('-')
        if g_info[0] == '2':
            d = int_or_str(g_info[1], data)
            if d:
                display_info(d)
            else:
                print('获取信息错误....请输入正确的名字或排名号')
        elif g_info[0] == '3':
            d = int_or_str(g_info[1], data)
            if d:
                downloadIMG(d)
            else:
                print('下载图片错误....请输入正确的名字或排名号')
        else:
            print('输入格式错误！')


def main():
    if not os.path.exists('img'):
        os.mkdir('img')
    if not os.path.exists('Movie250.csv'):
        print('正在获取豆瓣Top250信息，请稍等......')
        capAll()
        time.sleep(5)
        new_data = sorted(Moive, key=lambda x: x['Rnk'])
    else:
        new_data = read_from_csv()
    while True:
        input_info = input('请输入相应的数字(回车直接退出)\n'
                           '1(保存Top250到本地csv文件)\n'
                           '2-[排名]//[电影名](获取相关电影信息（列:2-66//2-国王的演讲[*2-为英文半角]）)\n'
                           '3-[排名]//[电影名](获取相关电影信息（列:3-66//3-国王的演讲[*3-为英文半角]）)\n'
                           '4（保存所有top250电影图片到本地)\n'
                           )
        if input_info == '1':
            save_as_csv(headers, new_data)
            print('正在保存请稍等.....')
            time.sleep(2)
            print('保存完毕！')
        elif '2-' in input_info:
            get_input(input_info, new_data)
        elif '3-' in input_info:
            get_input(input_info, new_data)
        elif input_info == '4':
            print('正在保存图片')
            get_all_img(new_data)
            time.sleep(2)
            print('图片保存完毕')
        else:
            break

if __name__ == '__main__':
    main()
