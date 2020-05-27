import requests
import time
import pymysql


def get_data(city_id):
    url = 'http://api.map.baidu.com/place/v2/search?query=交通设施&tag=收费站&region='+city_id+'&output=json&ak=4wAjx3T4AQtpbqfwuNByB83XkWWVhN0o'
    response = requests.get(url)
    soup = response.json()
    stations = soup['results']
    for station in stations:
        name = str(station['name'])
        lat = str(station['location']['lat'])
        lng = str(station['location']['lng'])
        address = str(station['address'])
        province = str(station['province'])
        city = str(station['city'])
        area = str(station['area'])
        connect_mysql(province, city, area, name, lat, lng, address)
    print("此地有收费站！")

def connect_mysql(province1, city1, area1, name1, lat1, lng1, address1):
    conent = pymysql.connect(host='localhost', user='root', passwd='root', db='station', charset='utf8')
    cursor = conent.cursor()
    print(province1 + ',' + city1 + ',' + area1 + ',' + name1 + ',' + lat1 + ',' + lng1 + ',' + address1)
    try:
        sql = """INSERT INTO station_info(Province,City,Area,Name,Lat,Lng,Address) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (province1, city1, area1, name1, lat1, lng1, address1)
        cursor.execute(sql)
        conent.commit()
    except pymysql.Error as e:
        print(e)

if __name__ == '__main__':
    lists = ['231', '232', '233', '323', '324', '284', '285', '170', '171', '352']
    for list in lists:
        get_data(list)
        time.sleep(5)
