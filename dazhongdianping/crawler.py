from connect_mysql import DataToMysql
from bs4 import BeautifulSoup
import requests
import time

#url = 'https://xa.meituan.com/s/火锅/'
def get_information(url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    response = requests.get(url,headers = headers,verify = False)
    soup = BeautifulSoup(response.text, 'lxml')

    titles = soup.select('.tit > a')
    stars = soup.select('span.sml-rank-stars')
    evalPeoples = soup.select('.comment > a')
    prices = soup.select('span.avg-price')
    addresses = soup.select('span.address')

    for title, evaluate, evalPeople, price, address in zip(titles, evaluates, evalPeoples, prices, addresses):
        data = {
            'tltle': title.get_text(),
            'evaluate': evaluate.get_text(),
            'evalPeople': evalPeople.get_text(),
            'price': price.get_text(),
            'address': address.get_text(),
            'time': time.strftime('%Y-%m-%d', time.localtime(time.time()))
        }
        print(data)
        mysql = DataToMysql('localhost', 'root', 'root', 'houseprice')
        mysql.write('huoguo', data)
