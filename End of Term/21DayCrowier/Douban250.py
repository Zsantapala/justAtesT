#-*-coding:utf:8-*-
import requests, csv, threading, time
Moive = []
headers = ['Rnk', 'id', 'title', 'casts', 'Moive_url', 'image']
def getMoive(data,rnk):
    global Movie
    try:
        M_info = {
            'Rnk': rnk,
            'id': data['id'],
            'title': data['title'],
            'casts': ','.join(c['name'] for c in data['casts']),
            'Moive_url': 'https://api.douban.com/v2/movie/{id}?apikey=0df993c66c0c636e29ecbb5344252a4a'.format(id=data['id']),
            'image': data['images']['small'],
        }
        Moive.append(M_info)
    except:
        print('getMovie Error')

def openUrl(num):
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

def capAll():
    ts1 = []
    for startnum in range(0, 250, 20):
        print('正在打开第%d个' %startnum)
        t1 = threading.Thread(target=openUrl, args=(startnum,))
        t1.start()
        ts1.append(t1)
    for t in ts1:
        t.join()

def save_as_csv(header,rows):
    try:
        with open('Movie250.csv', 'w', newline='') as f:
            f_csv = csv.DictWriter(f, header)
            f_csv.writeheader()
            f_csv.writerows(rows)
    except:
        print('saveError')

def downloadIMG(moive):
    try:
        picurl = moive['image']
        picname = 'img//' + moive['title']
        get_pic = requests.get(picurl).content
        with open(picname, 'wb') as img:
            img.write(get_pic)
    except:
        print('downloadImg Error')
def get_all_img(data):
    tm_s = []
    for img in range(len(data)):
        tm = threading.Thread(target=downloadIMG, args=(data[img],))
        tm.start()
        tm_s.append(tm)
    for t in tm_s:
        t.join()

if __name__ == '__main__':
    print('正在获取豆瓣Top250信息，请稍等......')
    capAll()
    time.sleep(5)
    new_data = sorted(Moive, key=lambda x: x['Rnk'])
    while True:
        pass
