#-*-coding:utf-8-*-
import requests, csv, time, threading
from bs4 import BeautifulSoup as bs

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

    def cra_web_desc(self, url):
        try:
            self.header['cookie'] = 'x-zp-client-id=dcbabdf3-aaa2-4fac-935a-1b1194e6b169; sts_deviceid=16d1efb093e372-01e3d41aa4652c-36664c08-1049088-16d1efb094694; sajssdk_2015_cross_new_user=1; dywea=95841923.2304648493983628500.1568182833.1568182833.1568182833.1; dywec=95841923; dywez=95841923.1568182833.1.1.dywecsr=crossincode.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/vip/homework/30/; sts_sg=1; sts_sid=16d1efb0daf1d-082a857fe3141f-36664c08-1049088-16d1efb0db02ed; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fcrossincode.com%2Fvip%2Fhomework%2F30%2F; jobRiskWarning=true; sou_experiment=unexperiment; ZP_OLD_FLAG=false; POSSPORTLOGIN=5; CANCELALL=1; LastCity=%E6%AD%A6%E6%B1%89; LastCity%5Fid=736; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216d1efb0d5342-0eb50658e71bd6-36664c08-1049088-16d1efb0d5436%22%2C%22%24device_id%22%3A%2216d1efb0d5342-0eb50658e71bd6-36664c08-1049088-16d1efb0d5436%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%22b116f277-9f9a-4137-8a5e-7d3a6b17104a-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22jobs%22:{%22recommandActionidShare%22:%22fee338b3-1460-498f-b9a8-6b7a51483aef-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sts_evtseq=19'
            reque_web = requests.get(url['job_url']+'l', headers=self.header).content
            web_soup = bs(reque_web, 'lxml')
            result = web_soup.find('div', attrs={'class': 'describtion'})
            if result:
                describe = ''
                for i in result.strings:
                    describe += i
                self.job_desc.append({
                    'job': url['job_Name'],
                    'describe': describe.replace(u'\xa0', u'')
                })
            else:
                print('requests web_describe error')
        except:
            print('cra_web_disc Error')

    def csv_job(self, work=1):
        try:
            if work == 1:
                csvHeader = ['company_name', 'company_type', 'company_size', 'job_Name', 'employee_type', 'edu_level', 'working_year', 'salary', 'job_url']
                with open('ZP_job.csv', 'w', newline='') as f:
                    f_csv = csv.DictWriter(f, csvHeader)
                    f_csv.writeheader()
                    f_csv.writerows(self.job)
            else:
                csvHeader = ['job', 'describe']
                with open('ZP_job_Describe.csv', 'w', newline='') as f:
                    f_csv = csv.DictWriter(f, csvHeader)
                    f_csv.writeheader()
                    f_csv.writerows(self.job_desc)
        except:
            print('Save Error!')

if __name__ == '__main__':
    cs = Zhao_Ping('wh')
    cs.cra_job()
    print('正在抓取信息请稍后......')
    time.sleep(3)
    print('一共获取到%d条记录' %len(cs.job))
    cs.csv_job()
    time.sleep(3)
    print('正在保存记录请稍等......')
    line = input('请输入想获取多少条记录\n')
    try:
        l = int(line)
    except ValueError:
        print('请输入正确数字')
    if 0 < l <= len(cs.job):
        ts = []
        for s in range(l):
            term = threading.Thread(target=cs.cra_web_desc, args=(cs.job[s],))
            term.start()
            ts.append(term)
        for t in ts:
            t.join()
    cs.csv_job(2)
    time.sleep(3)
    print('正在保存文件，请稍等')