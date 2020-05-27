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
                connect_mysql(station_id,times,float(td_list1[1]),float(td_list1[2]),float(td_list2[1]))
                td_list1 = []
                td_list2 = []

def connect_mysql(station_id,roadTime, roadFlow, roadOccupancy, roadSpeed):
    conent = pymysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'pems', charset = 'utf8')
    cursor = conent.cursor()
    # print(roadTime+','+roadFlow+','+roadOccupancy+','+roadSpeed)
    try:
        sql = """INSERT INTO pems_data_2018(Points,Times,Flow,Occupancy,Speed) VALUES ('%s','%s','%f','%f','%f')""" % (station_id, roadTime, roadFlow, roadOccupancy, roadSpeed)
        cursor.execute(sql)
        print(station_id+','+roadTime+','+str(roadFlow)+','+str(roadOccupancy)+','+str(roadSpeed))
        conent.commit()
    except pymysql.Error as e:
        print("数据已存在")

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

if __name__ == '__main__':

    url_f_o = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=400983&s_time_id=1520899200&s_time_id_f=03%2F13%2F2018+00%3A00&e_time_id=1521158400&e_time_id_f=03%2F16%2F2018+00%3A00&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=occ&gn=5min&agg=on&html.x=35&html.y=6'
    url_s = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=400983&s_time_id=1520899200&s_time_id_f=03%2F13%2F2018+00%3A00&e_time_id=1521158400&e_time_id_f=03%2F16%2F2018+00%3A00&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=speed&q2=occ&gn=5min&agg=on&html.x=48&html.y=5'

    id = '400983'
    get_data(id, url_f_o, url_s)
