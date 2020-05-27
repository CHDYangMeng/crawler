
from bs4 import BeautifulSoup
import requests
import time
from test3 import DataToMysql


def get_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    time.sleep(2)
    titles = soup.select('span.result_title')
    prices = soup.select('span.result_price > i')
    descriptions = soup.select('em.hiddenTxt')
    for title,price,description in zip(titles,prices,descriptions):
        data = {
            'title':title.get_text(),
            'price':price.get_text(),
            'descrition':description.get_text()
        }
        print(data)
        mysql = DataToMysql('localhost', 'root', 'root', 'test')
        mysql.write('xiaozhu', data)

def get_url(start,end):
    for i in range(start,end,1):
        urls = 'http://xa.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i))
        get_info(urls)

if __name__ == '__main__':
    get_url(2,10)


















