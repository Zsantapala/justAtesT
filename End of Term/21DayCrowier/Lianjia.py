#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup as bs
class Lianjia(object):
    def __init__(self):
        self.url = 'https://sh.lianjia.com/zufang/'
        self.getcontent = []