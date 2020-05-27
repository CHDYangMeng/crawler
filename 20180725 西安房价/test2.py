
from bs4 import BeautifulSoup
import requests
import time


# url = 'https://xa.fang.anjuke.com/?from=navigation/'
urls = ['https://xa.fang.anjuke.com/loupan/all/p{}/'.format(str(i)) for i in range(2,25,1)]

# we_web = requests.get(url)
# soup = BeautifulSoup(we_web.text,'lxml')
# print(soup)

def get_price(url,data=None):
    we_web = requests.get(url)
    time.sleep(4)
    soup = BeautifulSoup(we_web.text,'lxml')
    names = soup.select('.items-name')
    locals = soup.select('.list-map')
    prices = soup.select('p.price > span')
    tels = soup.select('.tel')
    for name,local,price,tel in zip(names,locals,prices,tels):
        data = {
            'name':name.get_text(),
            'local':local.get_text(),
            'price':price.get_text(),
            'tel':tel.get_text()
        }
        print(data)
for single_url in urls:
    get_price(single_url)



