#-*-coding:utf-8-*-
import requests, csv, time, threading, os
from bs4 import BeautifulSoup as bs
from selenium import webdriver

class Zhao_Ping():
    def __init__(self, cityname):
        self.city = {
            'bj': '530',
            'sh': '538',
            'sz': '765',
            'gz': '763',
            'cd': '801',
            'hz': '653',
            'tj': '531',
            'wh': '736',
        }
        self.url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={getcity}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&_v=0.13508793&x-zp-page-request-id=1d6ec2762812454e91395913689d1608-1568125299977-634376&x-zp-client-id=8ce635ff-0052-47a9-bb4e-753087b36897'.format(getcity=self.city[cityname])
        self.job = []
        self.job_desc = []
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        self.cookie_dic = {}

    def cra_job(self):
        try:
            content = requests.get(self.url, headers=self.header)
            content_date = content.json()['data']['results']
            for d in content_date:
                info = {
                    'company_name': d['company']['name'],
                    'company_type': d['company']['type']['name'],
                    'company_size': d['company']['size']['name'],
                    'job_Name': d['jobName'],
                    'employee_type': d['emplType'],
                    'edu_level': d['eduLevel']['name'],
                    'working_year': d['workingExp']['name'],
                    'salary': d['salary'],
                    'job_url': d['positionURL'],
                }
                self.job.append(info)
        except:
            print('cra_job error')

    def get_cookies(self):
        dirs = os.getcwd()
        files = dirs+'\\chromedriver.exe'
        dr = webdriver.Chrome(executable_path=files)
        for job in self.job:
            dr.get(job['job_url'])
            coo = dr.get_cookies()
            for c in coo:
                self.cookie_dic[c['name']] = c['value']
            time.sleep(10)
            if len(self.cookie_dic) > 1:
                return self.cookie_dic


    def cra_web_desc(self, url):
        try:
            reque_web = requests.get(url['job_url']+'l', headers=self.header, cookies=self.cookie_dic).content
            web_soup = bs(reque_web, 'lxml')
            result = web_soup.find('div', attrs={'class': 'describtion'})
            if result:
                describe = ''
                for i in result.strings:
                    describe += i
                self.job_desc.append({
                    'job': url['job_Name'],
                    'describe': describe.replace(u'\xa0', u'')   #gbk编码会遇错，&nbsp转为空白符
                })
            else:
                print('requests web_describe error')
        except:
            print('cra_web_disc Error')

    def csv_job(self, work=1):
        try:
            if work == 1:
                csvHeader = ['company_name', 'company_type', 'company_size', 'job_Name', 'employee_type', 'edu_level', 'working_year', 'salary', 'job_url']
                with open('ZP_job.csv', 'w', newline='', encoding='gb18030') as f:
                    f_csv = csv.DictWriter(f, csvHeader)
                    f_csv.writeheader()
                    f_csv.writerows(self.job)
            else:
                csvHeader = ['job', 'describe']
                with open('ZP_job_Describe.csv', 'w', newline='', encoding='gb18030') as f:
                    f_csv = csv.DictWriter(f, csvHeader)
                    f_csv.writeheader()
                    f_csv.writerows(self.job_desc)
        except:
            print('Save Error!')

if __name__ == '__main__':
    city = input('请输入想要查询的城市信息的城市名拼音缩写\n（例如：北京为bj，上海为sh,暂只支持北京、上海、深圳、广州、成都、杭州、天津、武汉8个城市)：\n')
    try:
        cs = Zhao_Ping(city.lower().strip())
        cs.cra_job()
        print('正在抓取信息请稍后......')
        time.sleep(3)
        print('一共获取到%d条记录' % len(cs.job))
        cs.csv_job()
        print('正在保存记录请稍等......')
        time.sleep(3)
        line = input('请输入想获取多少条记录\n')
        line_s = int(line)
        if 0 < line_s <= len(cs.job):
            if not cs.cookie_dic:
                cs.get_cookies()
            print(cs.cookie_dic)
            ts = []
            for s in range(line_s):
                term = threading.Thread(target=cs.cra_web_desc, args=(cs.job[s],))
                term.start()
                ts.append(term)
            for t in ts:
                t.join()
            if cs.job_desc:
                cs.csv_job(2)
                print('正在保存文件，请稍等')
                time.sleep(3)
                print('保存完毕！')
        else:
            print('条目数不多哦！')
    except KeyError or ValueError:
        print('输入城市信息错误,或输入页数错误')

