from bs4 import BeautifulSoup
import requests
import re
import json
# url = 'https://xa.meituan.com/meishi/c17/'

url = 'http://course-online.chd.edu.cn/course/3389/enrollments?tdsourcetag=s_pctim_aiomsg'
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Referer':
        'http://course-online.chd.edu.cn/course/3389/enrollments?tdsourcetag=s_pctim_aiomsg',
    'Host':
        'course-online.chd.edu.cn',
    'Cookie':
        'UM_distinctid=16b5548f01a8ca-0c35e06bbfe564-b79183d-1fa400-16b5548f01b90a; iPlanetDirectoryPro=AQIC5wM2LY4SfczpsSocivJ6HgfiLyo%2ByAx0Hk7cO3qYNGo%3D%40AAJTSQACMDI%3D%23; session=V2-1-9aee16c3-e497-4f23-ba24-374301f0e13d.MTAwMzQ2.1570681960.c1mtrxa03Tgn3opFoOxuOuXDm38'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
table = soup.select('')
