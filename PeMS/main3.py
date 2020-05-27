from bs4 import BeautifulSoup
import requests
# import pymysql
import time
import pandas


url_flow_occ = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=1119689&s_time_id=1420070400&s_time_id_f=01%2F01%2F2015+00%3A00&e_time_id=1420329540&e_time_id_f=01%2F03%2F2015+23%3A59&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=occ&gn=5min&agg=on&html.x=35&html.y=6'
url_speed = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=1119689&s_time_id=1420070400&s_time_id_f=01%2F01%2F2015+00%3A00&e_time_id=1420329540&e_time_id_f=01%2F03%2F2015+23%3A59&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=speed&q2=occ&gn=5min&agg=on&html.x=48&html.y=5'

headers = {
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Cookie':
                '__utma=158387685.1997529099.1544341664.1544341664.1544341664.1; __utmz=158387685.1544341664.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=267661199.1544342014.5.2.utmcsr=dot.ca.gov|utmccn=(referral)|utmcmd=referral|utmcct=/trafficops/mpr/source.html; PHPSESSID=e03d793a3c9b94632b6ccf6b9bf753ec; __utma=267661199.1806942116.1541166554.1545034185.1545201726.9; __utmc=267661199; __utmt=1; __utmb=267661199.14.10.1545201726'}

def getdata(url_f_o,url_s):
    '''
    :param url_f_o:
    :param url_s:
    :return: Times,Flow,Occupancy,Speed
    '''
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
    df = pandas.DataFrame()
    for table1,table2 in zip(tables1,tables2):
        for d1,d2 in zip(table1.find_all('td'),table2.find_all('td')):
            td_list1.append(d1.string)
            td_list2.append(d2.string)
            flag = flag + 1
            if flag % 5 == 0:
                data = {
                    '1time' : td_list1[0],
                    '2flow' : td_list1[1],
                    '3occupancy' : td_list1[2],
                    '4speed' : td_list2[1]
                }
                df = df.append(data, ignore_index=True)
                td_list1 = []
                td_list2 = []
    pandas.DataFrame(df).to_excel("I15-N.xlsx", sheet_name="I15-N", index=False, header=True)


if __name__=='__main__':
    getdata(url_flow_occ,url_speed)



























