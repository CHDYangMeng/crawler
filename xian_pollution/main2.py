# utf-8
from bs4 import BeautifulSoup
import requests
import pymysql


url_start = 'http://www.tianqihoubao.com/lishi/xian/month/201801.html'
headers = {
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            }

def getdata(url):
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    tems = soup.select('div.wdetail > table')
    list1 = []
    for tem in tems:
        flag = 0
        for d1 in tem.find_all('td'):
            flag = flag + 1
            try:
                list1.append(d1.text.strip())
            except:
                print(0)
            if flag%4 == 0:
               connect_mysql(list1[0],list1[1],list1[2],list1[3])
               list1 = []

def connect_mysql(date1, condition1, temperature1, wind1):
    conent = pymysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'xian_weather', charset = 'utf8')
    cursor = conent.cursor()
    print(date1+','+condition1+','+temperature1+','+wind1)
    try:
        sql = """INSERT INTO weather(date,condition,temperature,wind) VALUES ('%s','%s','%s','%s')""" % (date1, condition1, temperature1, wind1)
        cursor.execute(sql)
        print(date1+','+condition1+','+temperature1+','+wind1)
        conent.commit()
    except pymysql.Error as e:
        print(e)

if __name__ == '__main__':
    getdata(url_start)




