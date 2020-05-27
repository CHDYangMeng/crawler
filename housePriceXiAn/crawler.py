from connect_mysql import DataToMysql
from bs4 import BeautifulSoup
import requests
import time


def get_information(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    wb_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('.resblock-name > a')
    typess = soup.select('.resblock-type')
    locations = soup.select('.resblock-location')
    houseTypes = soup.select('.resblock-room')
    prices = soup.select('.main-price > span.number')

    for title, types, location, houseType, price in zip(titles, typess, locations, houseTypes, prices):
        data = {
            'title': title.get_text(),
            'type': types.get_text(),
            'location': location.get_text(),
            'houseType': houseType.get_text(),
            'price': price.get_text(),
            'time' : time.strftime('%Y-%m-%d',time.localtime(time.time()))
        }
        print(data)
        mysql = DataToMysql('localhost', 'root', 'root', 'houseprice')
        mysql.write('xian', data)


