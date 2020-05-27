from bs4 import BeautifulSoup
import requests
import pymysql
import time
import datetime

def get_data(station_id,url_f_o,url_s):
    '''
    :param url_f_o:
    :param url_s:
    :return: Times,Flow,Occupancy,Speed
    '''
    headers = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Cookie':
            '__utma=158387685.1997529099.1544341664.1544341664.1544341664.1; __utmz=158387685.1544341664.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=267661199.1552488912.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=07172e09f392ba389f455a81040a7fb6; __utmc=267661199; __utma=267661199.979179873.1552488912.1554375555.1554378590.20; __utmt=1; __utmb=267661199.1.10.1554378590'}
    '''
    获取单个检测器的交通流量与占有率
    '''
    res1 = requests.get(url_f_o, headers = headers)
    soup1 = BeautifulSoup(res1.text,'lxml')
    tables1 = soup1.select('table.inlayTable > tbody')
    print("交通流量与占有率提取成功")
    '''
    获取单个监测器的速度
    '''
    res2 = requests.get(url_s, headers=headers)
    soup2 = BeautifulSoup(res2.text, 'lxml')
    tables2 = soup2.select('table.inlayTable > tbody')
    print("速度提取成功")

    flag = 0
    td_list1 = []
    td_list2 = []
    for table1,table2 in zip(tables1,tables2):
        for d1,d2 in zip(table1.find_all('td'),table2.find_all('td')):
            td_list1.append(d1.string)
            td_list2.append(d2.string)
            flag = flag + 1
            if flag % 5 == 0:
                times = time_exchange(td_list1[0])
                if ',' in td_list1[1]:
                    t1 = td_list1[1].split(',')[0]
                    t2 = td_list1[1].split(',')[1]
                    td_list1[1] = t1 + t2
                print(station_id+','+times+','+td_list1[1]+','+td_list1[2]+','+td_list2[1])
                td_list1 = []
                td_list2 = []

def time_exchange(times):
    t1 = times.split(' ')
    date = t1[0]
    t2 = date.split('/')
    year = t2[2]
    month = t2[0]
    day = t2[1]
    time = t1[1]
    t_fin = year + '-' + month + '-' + day + ' ' + time + ':00'
    return t_fin

def get_url(station_id,startTime, stopTime):
    startTime_unix = time_unix(startTime)
    stopTime_unix = time_unix(stopTime)
    start_date_list = time_split(startTime)
    stop_date_list = time_split(stopTime)
    url_f_o = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id='+station_id+'&s_time_id='+startTime_unix+'&s_time_id_f='+start_date_list[1]+'%2F'+start_date_list[2]+'%2F'+start_date_list[0]+'+'+start_date_list[3]+'%3A'+start_date_list[4]+'&e_time_id='+stopTime_unix+'&e_time_id_f='+stop_date_list[1]+'%2F'+stop_date_list[2]+'%2F'+stop_date_list[0]+'+'+stop_date_list[3]+'%3A'+stop_date_list[4]+'&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=occ&gn=5min&agg=on&html.x=35&html.y=6'
    url_s = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id='+station_id+'&s_time_id='+startTime_unix+'&s_time_id_f='+start_date_list[1]+'%2F'+start_date_list[2]+'%2F'+start_date_list[0]+'+'+start_date_list[3]+'%3A'+start_date_list[4]+'&e_time_id='+stopTime_unix+'&e_time_id_f='+stop_date_list[1]+'%2F'+stop_date_list[2]+'%2F'+stop_date_list[0]+'+'+stop_date_list[3]+'%3A'+stop_date_list[4]+'&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=speed&q2=occ&gn=5min&agg=on&html.x=48&html.y=5'
    return url_f_o, url_s

def time_unix(times):
    date_time = datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S')
    date_time_8 = date_time + datetime.timedelta(hours=8)
    # date_time_8_str = date_time_8.strftime('%Y-%m-%d %H:%M:%S')
    unix_time = str(int(time.mktime(date_time_8.timetuple())))
    return unix_time

def time_split(times):
    date0 = times.split(' ')[0]
    date1 = times.split(' ')[1]
    year = date0.split('-')[0]
    month = date0.split('-')[1]
    day = date0.split('-')[2]
    hour = date1.split(':')[0]
    minuite = date1.split(':')[1]
    sceond = date1.split(':')[2]
    return year,month,day,hour,minuite,sceond

if __name__ == '__main__':
    station_id = '400075'
    start_date_str = '2018-03-11 00:00:00'
    stop_date_str = '2018-03-12 00:00:00'
    url_list = get_url(station_id, start_date_str, stop_date_str)
    print(url_list[0])
    get_data(station_id, url_list[0], url_list[1])