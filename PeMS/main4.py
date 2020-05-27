from bs4 import BeautifulSoup
import requests
import pymysql
import time
import datetime

def get_data(url_f_o,url_s):
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
            '__utma=158387685.1997529099.1544341664.1544341664.1544341664.1; __utmz=158387685.1544341664.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=267661199.1552488912.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=d04dfdf997c762060ed6183c8adee7e4; __utma=267661199.979179873.1552488912.1552807059.1552830955.3; __utmc=267661199; __utmt=1; __utmb=267661199.6.10.1552830955'}
    '''
    获取单个检测器的交通流量与占有率
    '''
    res1 = requests.get(url_f_o, headers = headers)
    soup1 = BeautifulSoup(res1.text,'lxml')
    tables1 = soup1.select('table.inlayTable > tbody')
    '''
    获取单个监测器的速度
    '''
    res2 = requests.get(url_s, headers=headers)
    soup2 = BeautifulSoup(res2.text, 'lxml')
    tables2 = soup2.select('table.inlayTable > tbody')

    flag = 0
    td_list1 = []
    td_list2 = []
    for table1,table2 in zip(tables1,tables2):
        for d1,d2 in zip(table1.find_all('td'),table2.find_all('td')):
            td_list1.append(d1.string)
            td_list2.append(d2.string)
            flag = flag + 1
            if flag % 5 == 0:
                connect_mysql(td_list1[0],td_list1[1],td_list1[2],td_list2[1])
                td_list1 = []
                td_list2 = []

def connect_mysql(roadTime, roadFlow, roadOccupancy, roadSpeed):
    conent = pymysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'pems', charset = 'utf8')
    cursor = conent.cursor()
    print(roadTime+','+roadFlow+','+roadOccupancy+','+roadSpeed)
    try:
        sql = """INSERT INTO i15_n(Times,Flow,Occupancy,Speed) VALUES ('%s','%s','%s','%s')""" % (roadTime, roadFlow, roadOccupancy,roadSpeed)
        cursor.execute(sql)
        print(roadTime+','+roadFlow+','+roadOccupancy+','+roadSpeed)
        conent.commit()
    except pymysql.Error as e:
        print(e)
# id=400075
def get_url(startTime, stopTime):
    startTime_unix = time_unix(startTime)
    stopTime_unix = time_unix(stopTime)
    start_date_list = time_split(startTime)
    stop_date_list = time_split(stopTime)
    url_f_o = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=400075&s_time_id='+startTime_unix+'&s_time_id_f='+start_date_list[1]+'%2F'+start_date_list[2]+'%2F'+start_date_list[0]+'+'+start_date_list[3]+'%3A'+start_date_list[4]+'&e_time_id='+stopTime_unix+'&e_time_id_f='+stop_date_list[1]+'%2F'+stop_date_list[2]+'%2F'+stop_date_list[0]+'+'+stop_date_list[3]+'%3A'+stop_date_list[4]+'&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=occ&gn=5min&agg=on&html.x=35&html.y=6'
    url_s = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=400075&s_time_id='+startTime_unix+'&s_time_id_f='+start_date_list[1]+'%2F'+start_date_list[2]+'%2F'+start_date_list[0]+'+'+start_date_list[3]+'%3A'+start_date_list[4]+'&e_time_id='+stopTime_unix+'&e_time_id_f='+stop_date_list[1]+'%2F'+stop_date_list[2]+'%2F'+stop_date_list[0]+'+'+stop_date_list[3]+'%3A'+stop_date_list[4]+'&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=speed&q2=occ&gn=5min&agg=on&html.x=48&html.y=5'
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

if __name__=='__main__':
    flag = 0
    start_date_str = '2018-01-01 00:00:00'
    stop_date_str = '2019-01-01 23:59:00'
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
    stop_date = datetime.datetime.strptime(stop_date_str, '%Y-%m-%d %H:%M:%S')
    if (stop_date - start_date).days > 3:
        while (stop_date - start_date).days > 3:
            time.sleep(10)
            start_date1 = start_date
            stop_date = stop_date
            stop_date1 = start_date1 + datetime.timedelta(days=3)
            start_date2 = start_date1.strftime('%Y-%m-%d %H:%M:%S')
            stop_date2 = stop_date1.strftime('%Y-%m-%d %H:%M:%S')
            url_list = get_url(start_date2,stop_date2)
            get_data(url_list[0], url_list[1])
            start_date = stop_date1
            flag = flag + 1
            if flag % 10 == 0:
                time.sleep(30)

        url_list = get_url(start_date.strftime('%Y-%m-%d %H:%M:%S'), stop_date.strftime('%Y-%m-%d %H:%M:%S'))
        get_data(url_list[0], url_list[1])
    else:
        url_list = get_url(start_date.strftime('%Y-%m-%d %H:%M:%S'), stop_date.strftime('%Y-%m-%d %H:%M:%S'))
        get_data(url_list[0], url_list[1])







    # url_flow_occ = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=1119689&s_time_id=1420070400&s_time_id_f=01%2F01%2F2015+00%3A00&e_time_id=1420329540&e_time_id_f=01%2F03%2F2015+23%3A59&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=occ&gn=5min&agg=on&html.x=35&html.y=6'
    # url_speed = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=1119689&s_time_id=1420070400&s_time_id_f=01%2F01%2F2015+00%3A00&e_time_id=1420329540&e_time_id_f=01%2F03%2F2015+23%3A59&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=speed&q2=occ&gn=5min&agg=on&html.x=48&html.y=5'




























