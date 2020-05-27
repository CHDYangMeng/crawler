
from bs4 import BeautifulSoup
import requests
import time
import pymysql

# 104.166102,31.707044
# 111.469829,39.763705

# 108.880409,34.220028
# 108.912245,34.234057
# url = 'http://api.map.baidu.com/place/v2/search?query=收费站&bounds=34.220028,108.880409,34.234057,108.912245&output=json&ak=4wAjx3T4AQtpbqfwuNByB83XkWWVhN0o'


# names = soup['results'][0]['name']
# lat = soup['results']['location'][0]
# lon = soup['results']['location'][1]
# print(names)

def get_station(left_lon, left_lat, right_lon, right_lat, flag3):
    flag1 = 1
    if ((right_lat - left_lat > 0.1) & (right_lon - left_lon > 0.1)):
        while (right_lon > left_lon):
            left_lat_t = left_lat
            flag2 = 0
            while (right_lat > left_lat_t):
                right_lat_new = left_lat_t + 0.5
                right_lon_new = left_lon + 0.5
                left_lat_str = str(left_lat_t)
                left_lon_str = str(left_lon)
                right_lat_str = str(right_lat_new)
                right_lon_str = str(right_lon_new)
                get_data(left_lat_str, left_lon_str, right_lat_str, right_lon_str)
                left_lat_t = right_lat_new
                time.sleep(5)
                flag2 = flag2 + 1
                # print("爬起第" + str(flag1) + "行" + ",第" + str(flag2) + "列")
                print(flag3)
                flag3 = flag3 + 1
            left_lon = left_lon + 0.5
            flag1 = flag1 + 1
    else:
        left_lat_str = str(left_lat)
        left_lon_str = str(left_lon)
        right_lat_str = str(right_lat)
        right_lon_str = str(right_lon)
        get_data(left_lat_str, left_lon_str, right_lat_str, right_lon_str)

def get_data(left_lat,left_lon,right_lat,right_lon):
    url = 'http://api.map.baidu.com/place/v2/search?query=交通设施&tag=收费站&bounds='+left_lat+','+left_lon+','+right_lat+','+right_lon+'&output=json&ak=4wAjx3T4AQtpbqfwuNByB83XkWWVhN0o'
    response = requests.get(url)
    soup = response.json()
    stations = soup['results']
    if len(stations):
        # print(stations)
        for station in stations:
            try:
                name = str(station['name'])
                lat = str(station['location']['lat'])
                lng = str(station['location']['lng'])
                address = str(station['address'])
                province = str(station['province'])
                city = str(station['city'])
                area = str(station['area'])
            except KeyError as e:
                name = 'KeyError'
                lat = '0'
                lng = '0'
                address = ''
                province = ''
                city = ''
                area = ''
            connect_mysql(province, city, area, name, lat, lng, address)
    else:
        print(" ")

def connect_mysql(province1,city1,area1,name1,lat1,lng1,address1):
    conent = pymysql.connect(host='localhost', user='root', passwd='root', db='station', charset='utf8')
    cursor = conent.cursor()
    print(province1 + ',' + city1 + ',' + area1 + ',' + name1 + ',' + lat1 + ',' + lng1 + ',' + address1)
    try:
        sql = """INSERT INTO station_info_1(Province,City,Area,Name,Lat,Lng,Address) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (province1, city1, area1, name1, lat1, lng1, address1)
        cursor.execute(sql)
        conent.commit()
    except pymysql.Error as e:
        print(e)

if __name__ == '__main__':
    print("开始爬取数据!")
    start_time = time.time()
    get_station(104.166102, 31.707044, 111.469829, 39.763705, 1)
    end_time = time.time()
    print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))




