#-*-coding:utf-8-*-
import requests, csv

class ZhiHu(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
        'cookie': '_xsrf=BwHpHkR3ct1UrdGWV2VgfRvggjxyi25K; _zap=558d79a4-a1a9-40ac-a314-0891fb5e25e5; d_c0="APBif_Du0A6PTtSjq01EMzSOHJURp5xVXvk=|1547319448"; capsion_ticket="2|1:0|10:1566974136|14:capsion_ticket|44:YzYwYzJhMzQ3NmMzNGI1YzljZmNiYzU5NzkxN2Y2ZTc=|9657486a8a0132c884157a965c53a4530918ef1618208d307a7f4f3f419a795b"; z_c0="2|1:0|10:1566974152|4:z_c0|92:Mi4xM1dzWUF3QUFBQUFBOEdKXzhPN1FEaWNBQUFDRUFsVk55SzJOWFFEcThhLURndkN3Um5SbmxGMklWelRtd2tqbTBn|1c92571dbd9ab136529a6fd4016c9736018ebffcc0002fd71bd61fd85af3be66"; q_c1=42ea74b484ff466086975ac24ff4b25a|1567006261000|1548774405000; tshl=; tst=r; tgw_l7_route=116a747939468d99065d12a386ab1c5f',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
              }
        self.metaData= []
        self.content = []
    def requ_ZH(self, urls):
        try:
            r = requests.get(urls, headers=self.headers)
            result = r.json()
            self.metaData.append(result['data'])
            return result['paging']
        except:
            print('request Error')
            return

    def middle_data(self):
        for data in self.metaData:
            for d in data:
                if d['target']['type'] == 'article':
                    mid_data = [d['id'], d['action_text'], d['target']['voteup_count'], d['target']['title']]
                    self.content.append(mid_data)
                elif d['target']['type'] == 'answer':
                    mid_data = [d['id'], d['action_text'], d['target']['voteup_count'], d['target']['question']['title']]
                    self.content.append(mid_data)

    def rqe_ZH_more(self, num):
        url = self.url
        for count in range(num):
            result = self.requ_ZH(url)
            if result and result['next']:
                url = result['next']
            else:
                print('page is end')
                break

    def save_csv(self):
        self.middle_data()
        try:
            with open('zhihu.csv', 'w', newline='') as csv_f:
                f = csv.writer(csv_f)
                f.writerows(self.content)
        except:
            print('save_csv Error')

if __name__ == '__main__':
    url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=eb8ea7a27848ff2d3d94882a4f272c3d&desktop=true&page_number=2&limit=6&action=down&after_id=5'
    get_zhihu = ZhiHu(url)
    get_zhihu.rqe_ZH_more(5)
    get_zhihu.save_csv()