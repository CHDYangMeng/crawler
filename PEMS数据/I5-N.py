from bs4 import BeautifulSoup
import requests
import pymysql

url_flow = 'http://pems.dot.ca.gov/?report_form=1&dnode=VDS&content=loops&tab=det_timeseries&export=&station_id=1119689&s_time_id=1544572800&s_time_id_f=12%2F12%2F2018+00%3A00&e_time_id=1545173940&e_time_id_f=12%2F18%2F2018+22%3A59&tod=all&tod_from=0&tod_to=0&dow_0=on&dow_1=on&dow_2=on&dow_3=on&dow_4=on&dow_5=on&dow_6=on&holidays=on&q=flow&q2=&gn=5min&agg=on&lane1=on&lane2=on&lane3=on&lane4=on&html.x=47&html.y=10'
get_flow = 'flow'


headers = {
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Cookie':
                '__utma=158387685.1997529099.1544341664.1544341664.1544341664.1; __utmz=158387685.1544341664.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=267661199.1544342014.5.2.utmcsr=dot.ca.gov|utmccn=(referral)|utmcmd=referral|utmcct=/trafficops/mpr/source.html; PHPSESSID=e03d793a3c9b94632b6ccf6b9bf753ec; __utma=267661199.1806942116.1541166554.1545034185.1545201726.9; __utmc=267661199; __utmt=1; __utmb=267661199.14.10.1545201726'}

def getdata(url,name):
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tables = soup.select('table.inlayTable > tbody')
    flag = 0
    td_list = []
    table_name = name
    for table in tables:
        for d in table.find_all('td'):
            td_list.append(d.string)
            flag = flag + 1
            if flag%8 == 0:
                print(td_list[0])
                connect_mysql(table_name,td_list[0],td_list[5])
                td_list = []

# td_list[0],td_list[5]
def connect_mysql(tabel_name,roadtime,roadflow):
    connent = pymysql.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'pems', charset = 'utf8')
    cursor = connent.cursor()

    try:
        sql = """INSERT INTO '%s' (time,flow) VALUES ('%s','%s')""" % (tabel_name,roadtime, roadflow)
        cursor.execute(sql)
        connent.commit()
    except pymysql.Error as e:
        if str(e).split(',')[0].split('(')[1] == "1062":
            sql_del = """DELETE FROM '%s'""" % (tabel_name)
            cursor.execute(sql_del)
            sql_add = """INSERT INTO '%s' (time,flow) VALUES ('%s','%s')""" % (tabel_name,roadtime, roadflow)
            cursor.execute(sql_add)
            connent.commit()
        elif str(e).split(',')[0].split('(')[1] == "1146":
            # time_1 = 'time' + ' ' + 'varcahr(20)' + ','
            # flow_1 = 'flow' + ' ' + 'varchar(20)'
            # sql_cre = """CREATE TABLE flow ('%s','%s')""" % (time_1,flow_1)
            # cursor.execute(sql_cre)
            # sql_add = """INSERT INTO flow (time,flow) VALUES ('%s','%s')""" % (roadtime, roadflow)
            # cursor.execute(sql_add)
            # connent.commit()
            print(e)
if __name__=='__main__':
    getdata(url_flow,get_flow)






