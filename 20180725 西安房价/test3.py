
from bs4 import BeautifulSoup
import time
import requests

url = 'https://weheartit.com/recent?scrolling=true&page='

def get_info(url,data=None):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('.text-big')
    imgs = soup.select('.entry-thumbnail')
    cases = soup.select('.js-heart-count')

    for title,img,case in zip(titles,imgs,cases):
        data = {
            'title':title.get_text(),
            'img':img.get('src'),
            'case':case.get_text()
        }
        print(data)
def set_page(start,end):
    for one in range(start,end):
        get_info(url + str(one))
        time.sleep(2)

set_page(1,10)