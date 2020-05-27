
import requests
from bs4 import BeautifulSoup

headers = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Cookie':
            '__utma=158387685.1997529099.1544341664.1544341664.1544341664.1; __utmz=158387685.1544341664.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=267661199.1552488912.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHPSESSID=3941e736a01e0194674a190fa3f4898a; __utma=267661199.979179873.1552488912.1553862981.1554040262.13; __utmc=267661199; __utmt=1; __utmb=267661199.2.10.1554040262'}
'''
获取单个检测器的交通流量与占有率
'''

url_f_o = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=401698&s_time_id=1515024000&s_time_id_f=01%2F04%2F2018+00%3A00&e_time_id=1515283200&e_time_id_f=01%2F07%2F2018+00%3A00&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=occ&gn=5min&agg=on&html.x=35&html.y=6'
res1 = requests.get(url_f_o, headers = headers)
soup1 = BeautifulSoup(res1.text,'lxml')
tables1 = soup1.select('table.inlayTable > tbody')
td_list1 = []
flag = 0
for table1 in tables1:
    for d1 in table1.find_all('td'):
        td_list1.append(d1.string)
        flag = flag + 1
        if flag % 5 == 0:
            if ',' in td_list1[1]:
                t1 = td_list1[1].split(',')[0]
                t2 = td_list1[1].split(',')[1]
                td_list1[1] = t1 + t2
            print(td_list1[0]+','+td_list1[1] + ',' + td_list1[2])
            td_list1 = []