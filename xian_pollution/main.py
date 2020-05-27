# utf-8
from bs4 import BeautifulSoup
import requests
from datetime import date, time, datetime, timedelta
import pymysql


def get_data(url):
    headers = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    date = soup.select('div.live_data_time > p')
    data = soup.select('.value')
    date_time = date[0].text.split('：')[1]
    AQI = data[0].text.replace(' ', '').strip()
    PM25 = data[1].text.replace(' ', '').strip()
    PM10 = data[2].text.replace(' ', '').strip()
    CO = data[3].text.replace(' ', '').strip()
    NO2 = data[4].text.replace(' ', '').strip()
    O3 = data[5].text.replace(' ', '').strip()
    SO2 = data[6].text.replace(' ', '').strip()
    connect_mysql(date_time,AQI,PM25,PM10,CO,NO2,O3,SO2)

def connect_mysql(date_time1,AQI1,PM251,PM101,CO1,NO21,O31,SO21):
    conent = pymysql.connect(host='localhost', user='root', passwd='root', db='aqi_ontime', charset='utf8')
    cursor = conent.cursor()
    print(date_time1+','+AQI1+','+PM251+','+PM101+','+CO1+','+NO21+','+O31+','+SO21)
    try:
        sql = """INSERT INTO aqi_time(date_time,AQI,PM25,PM10,CO,NO2,O3,SO2) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')""" % (date_time1,AQI1,PM251,PM101,CO1,NO21,O31,SO21)
        cursor.execute(sql)
        conent.commit()
    except pymysql.Error as e:
        print(e)

def runTask(url):
    # Init time
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    # print("now:", strnow)
    get_data(url)
    period = timedelta(hours=1)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("next run:", strnext_time)
    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("start work: %s" % iter_now_time)
            get_data(url)
            print("task done.")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("next_iter: %s" % strnext_time)
            # Continue next iteration
            continue

if __name__ == '__main__':
    url_start = 'http://pm25.in/xian'
    runTask(url_start)

