from bs4 import BeautifulSoup
import requests
import time

# url = 'http://zg.58.com/shouji/34869997132610x.shtml'
# url = 'http://sz.58.com/shouji/34817934897486x.shtml'
def get_url(sell = 0):
    urls = []
    list_view = 'http://xa.58.com/iphonesj/{}/'.format(str(sell))
    wb_data = requests.get(list_view)
    time.sleep(2)
    soup = BeautifulSoup(wb_data.text,'lxml')
    href = soup.select('a.t')
    for link in href:
        urls.append(link.get('href'))
    return urls

# list_view = 'http://xa.58.com/iphonesj/0/'
# wb_data = requests.get(list_view)
# soup = BeautifulSoup(wb_data.text,'lxml')
# href = soup.select('a.t')
# print(href)


def get_info():
    urls = get_url()
    time.sleep(2)
    for url in urls:
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        data = {
            'title':soup.select('h1')[0].get_text(),
            'price':soup.select('.c_f50')[0].get_text() if soup.find_all('span','price') else None,
            'date':soup.select('.time')[0].get_text(),
            'local':soup.select('.c_25d')[0].get_text() if soup.find_all('span','c_25d') else None
        }
        print(data)

get_info()



# wb_data = requests.get(url)
# soup = BeautifulSoup(wb_data.text,'lxml')
# title = soup.select('h1')[0].text
# price = soup.select('.c_f50')[0].text
# date = soup.select('.time')[0].text
# local = soup.select('.c_25d > a')[0].get_text()
#
# print(title,price,date,local)


















