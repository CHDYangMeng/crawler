
from connect_sql import DataToMysql
from bs4 import BeautifulSoup
import requests

def get_information(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('.resblock-name > a')
    typess = soup.select('.resblock-type')
    states = soup.select('.sale-status')
    locations = soup.select('.resblock-location > a')
    prices = soup.select('.main-price > span.number')

    for title,types,state,location,price in zip(titles,typess,states,locations,prices):
        data = {
            'title':title.get_text(),
            'type':types.get_text(),
            'state':state.get_text(),
            'location':location.get_text(),
            'price':price.get_text(),
        }
        print(data)
        mysql = DataToMysql('localhost', 'root', 'root', 'test')
        mysql.write('xian_city', data)