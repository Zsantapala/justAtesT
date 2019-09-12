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
        #try:
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
        #except:
            #print('cra_job error')

    def cra_web_desc(self, url):
        try:
            self.header['cookie'] = 'x-zp-client-id=8ce635ff-0052-47a9-bb4e-753087b36897; sts_deviceid=16b41bddc422a0-05be91b735f228-43450521-2073600-16b41bddc434; \
            dywez=95841923.1560176114.1.1.dywecsr=landing.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/register; \
            sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22617712991%22%2C%22%24device_id%22%3A%2216b41bddc6517e-050d2585b6e578-43450521-2073600-16b41bddc6a486%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidupcpz%22%2C%22%24latest_utm_medium%22%3A%22cpt%22%7D%2C%22first_id%22%3A%2216b41bddc6517e-050d2585b6e578-43450521-2073600-16b41bddc6a486%22%7D; zg_did=%7B%22did%22%3A%20%2216b41be910d2e2-0ce003dc0ce487-43450521-1fa400-16b41be910f613%22%7D;\
             zg_08c5bcee6e9a4c0594a5d34b79b9622a=%7B%22sid%22%3A%201560176136467%2C%22updated%22%3A%201560176136473%2C%22info%22%3A%201560176136471%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22special.zhaopin.com%22%7D; urlfrom2=121126445; adfcid2=none; adfbid2=0; sou_experiment=unexperiment; LastCity=%E6%AD%A6%E6%B1%89; LastCity%5Fid=736; ZP_OLD_FLAG=false; POSSPORTLOGIN=6; CANCELALL=0; acw_tc=2760828c15680433593261380e3d1cb86e57726240f400329d271d1f29ebd5; dywea=95841923.2859570717331130400.1560176114.1568038854.1568125289.3; sts_sg=1; sts_chnlsid=Unknown; jobRiskWarning=true;\
              zp_src_url=https%3A%2F%2Fjobs.zhaopin.com%2FCC465262917J00318634704.htm; at=967fe92e2c704cfb8c212c6eed416835; rt=c3f87f45bcfe4c54ad0f3f8da97b0d6c; acw_sc__v2=5d79d8e1e74bbe957b13d374c5a9a7bd651908b0; sts_sid=16d23f7465a151-06a6046f933a5c-43450521-2073600-16d23f7465b4b5; privacyUpdateVersion=2; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22b86d0a0f-2e7e-48ab-a1a6-0f4bdc6cad3c-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sts_evtseq=8'
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
        #try:
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
        #except:
            #print('Save Error!')

if __name__ == '__main__':
    cs = Zhao_Ping('bj')
    cs.cra_job()
    print('正在抓取信息请稍后......')
    print(cs.job)
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