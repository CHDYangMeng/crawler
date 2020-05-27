
from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
apartment = client['apartment']
xian_apartment = apartment['xian_apartment']

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
        xian_apartment.insert_one(data)

def get_url():
    for i in range(2,5,1):
        urls = 'http://xa.xiaozhu.com/search-duanzufang-p{}-0/'.format(str(i))
        get_info(urls)



















