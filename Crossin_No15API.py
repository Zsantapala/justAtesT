#-*-coding:utf:8-*-
#!/usr/bin/python
import requests, re

class Lookup_Phone(object):
    def __init__(self,pnum=''):
        self.Pnum = pnum
        self.info = {}
        self.url = 'https://way.jd.com/jisuapi/query4?shouji='
        self.token = 'c525ee7fd114500ff3090d946bbc17a0'
        self.head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
        self.errorCode = {
            '10000': '查询成功',
            '10003': '不存在相应的数据信息',
            '10020': '万象系统繁忙，请稍后再试!',
            '10030': '调用万象网关失败， 请与万象联系',
            '10040': '超过每天限量，请明天继续',
            '10050': '用户已被禁用',
            '10060': '提供方设置调用权限，请联系提供方',
        }

    def getinfo(self):
        if self.Pnum == '':
            return 'please input right Phonenumber!'
        url = self.url + self.Pnum + '&appkey=' + self.token
        try:
            content = requests.get(url, headers=self.head).json()
        except :
            print ('get_content_error')
        else:
             self.info = content

    def disinfo(self):
        if self.info:
            Ecode = self.info['code']
            if Ecode == '10000':
                province = self.info['result']['result']['province']
                city = self.info['result']['result']['city']
                company = self.info['result']['result']['company']
                return 'Your Phonenumber is '+province+' '+city+' '+company
            else:
                return self.errorCode[Ecode]
        else:
            return ('somehting is wrong!')

if __name__ == '__main__':
    while True:
        phnum = input('please input  phone number:\n')
        check = re.search(r'^1\d{10}\b', phnum)
        if check and phnum == check.group():
            P = Lookup_Phone(phnum)
            P.getinfo()
            print (P.disinfo())
        elif phnum == '':
            print ('program out!')
            break
        else:
            print ('please input the right phone number!!\n')



