from bs4 import BeautifulSoup
import requests
import time
import datetime
import os
from numpy import unicode


def get_link(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('#list > dl > dd > a')
    for link in links:
        link_1 = link.get('href')
        get_info('http://www.biquge.com.tw' + link_1)

def get_info(url):
    wb_data = requests.get(url)
    wb_data.encoding = 'gbk'
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text,'lxml')
    title = soup.select('.bookname > h1')[0].get_text()
    download(title)
    contents = soup.select('#content')
    for content in contents:
        con = content.get_text().split()
        for i in con:
            download(i)
    procety(title)

def download(contents):
    with open('E:\\crawler\\20180729_novle\\圣墟.txt','a') as f:
        f.write(contents)
        f.close()

def procety(title):
    filePath = unicode('E:\\crawler\\20180729_novle\\圣墟.txt')
    fsize = os.path.getsize(filePath)
    fsize_1 = fsize/float(1024*1024)
    size = round(fsize_1,2)
    print('下载到' + title + ',' + str(size) + 'MB')

if __name__=='__main__':

    url = 'http://www.biquge.com.tw/11_11850/'
    get_link(url)
