
import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def get_movie_review(flag):
    for i in range(1,78):
        url = 'https://movie.douban.com/subject/24852545/reviews?start='+str(i*20)
        time.sleep(1)
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept':
                'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept - Encoding':
                'gzip, deflate, br',
            'Accept-Language':
                ':zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2'
        }
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        reviews = soup.select('.short-content')
        for review in reviews:
            concent = review.get_text().strip()
            download(flag, concent)
            flag = flag + 1

def download(flag,content):
    path = 'E:\\crawler\\20180809_auto\\movie_review\\爱情公寓影评_豆瓣.txt'
    with open(path ,'a',encoding='utf-8') as f:
        f.write(content)
        f.close()

        print('下载到第:'+str(flag)+'条影评')

if __name__=='__main__':
    flag = 1
    get_movie_review(flag)
