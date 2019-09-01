#-*-coding:utf-8-*-
import requests, csv
from bs4 import BeautifulSoup as bs
class Lianjia(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Chrome/69.0.3497.100',
            'Cookie': 'lianjia_ssid=7e8cccf7-2b61-46fa-9dd5-85b5c63be5fb; lianjia_uuid=c6353572-fec8-4382-bd51-56cae989399c; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMTMxOTgzYWYwNjkzODg3ZjhmZTU4M2M3Zjk1MmNmYzkzZjc5Y2RlM2E5ODFmNjgyNmY4ZWY2ZDc2OWIyMDMzYzVhYmJkMzZlZTM2ZTllNGYwZjc5ZmU4MTFhYjM4OTgyYjk0NDU1MDA2ZWMxZjA4ZTJiYjNmMDVkMzM2ZjBlYmU0YjdmMzc5OWFhY2E4NzNlN2I0Mjc5N2RmMTViNTdhYjg2MmJiOTA2NDJjYjBiYWQyZjI4YjZmYmQ2MzI2NDAwZjA0YTk3ZTQ5NzMxZTY5MGE1MDBiZDQ4M2Y2MDRhOGVlOWQ5MzczZWFlNTYwNWY4ZmMyMzJhODk5NjQ4OTdkM2UwYmZiYTVkYTIzNGQ0NjA4ODc1OGU1MTE1ZGMxMmJlNTFlYjE0YWE3MmU0YTQ4NjQ5MGVhNjIzY2Q4MjYzOWU0NjA4NTNkMjAzMzUxYTA3MjhiZjlkOTFkNTAyYzJkM1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIyMGUxNmM4ZVwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL3p1ZmFuZy8iLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
        }
        self.csvHeader = ['describe', 'url', 'place', 'area', 'Orientation', 'type', 'level', 'info', 'price']
        self.getcontent = []

    def req_url(self, url):
        try:
            get_web = requests.get(url, headers=self.header)
            if get_web.status_code == 200:
                return get_web.text
            else:
                print('response success but the server return isn\'t 200')
                return False
        except:
            print('request Error')
            return False

    def bs_html(self, content):
        html_soup = bs(content, 'lxml')
        get_element = html_soup.find_all('div', attrs={'class': 'content__list--item--main'})
        if get_element:
           for g in get_element:
               ele1 = g.find('p', attrs={'class': 'content__list--item--title twoline'})
               ele2 = g.find('p', attrs={'class': 'content__list--item--des'})
               ele3 = g.find('p', attrs={'class': 'content__list--item--bottom oneline'})
               ele4 = g.find('span', attrs={'class': 'content__list--item-price'})
               url1 = 'https://sh.lianjia.com'
               if ele1 and ele2 and ele3 and ele4:
                   ele2_c = ''.join([x.strip().replace(' ', '') for x in ele2.strings if x.strip() != '']).split('/')
                   cont_d = {
                       'describe': ele1.a.string.strip('\n').strip(),
                       'url': url1 + ele1.a['href'],
                       'place': ele2_c[0],
                       'area': ele2_c[1],
                       'Orientation': ele2_c[2],
                       'type': ele2_c[3],
                       'level': ele2_c[4],
                       'info': ' '.join([x.strip('\n') for x in ele3.strings]),
                       'price': ''.join([x for x in ele4.strings]),
                   }
                   self.getcontent.append(cont_d)
        else:
            print('soup find_all Error Find Noting ')
            return False

    def save_csv(self):
        try:
           with open('Lianjia.csv', 'w', newline='') as f:
               f_csv = csv.DictWriter(f, self.csvHeader)
               f_csv.writeheader()
               f_csv.writerows(self.getcontent)
        except:
            print('Save Error!')

if __name__ == '__main__':
    LJ = Lianjia()
    while True:
        print('租房信息一共有100页请输入开始页数（如果只取一页开始结束页数相同）\n')
        start = input('start:')
        print('租房信息一共有100页请输入结束页数（如果只取一页开始结束页数相同）\n')
        end = input('end:')
        print('正在获取，请稍后.......')
        try:
            s = int(start)
            e = int(end)
            if s == e:
                url = 'https://sh.lianjia.com/zufang/pg{value}/#contentList'.format(value=s)
                LJ.bs_html(LJ.req_url(url))
                LJ.save_csv()
                print('获取成功，文件已保存')
                break
            elif 0 < s < e <101:
                for i in range(s, e):
                    url = 'https://sh.lianjia.com/zufang/pg{value}/#contentList'.format(value=i)
                    LJ.bs_html(LJ.req_url(url))
                LJ.save_csv()
                print('获取成功，文件已保存')
                break
            else:
                print('输入错误！')
                continue
        except ValueError:
            print('输入错误！请重新输入......')
            continue

