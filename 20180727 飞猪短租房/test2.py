from bs4 import BeautifulSoup
import requests
import pymongo
import time


client = pymongo.MongoClient('localhost',27017)
phone = client['phone']
sheet_tab = phone['sheet_tab']
sheet_tab_1 = phone['sheet_tab_1']

def get_info():
    for i in range(60,300,60):
        url = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.10.5c03338bx4grdq&s={}&q=%D0%A1%C3%D7%CA%D6%BB%FA&sort=s&style=g&from=mallfp..pc_1_suggest&suggest=0_9&smAreaId=610100&type=pc#J_Filter'.format(str(i))
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        time.sleep(2)
        titles = soup.select('p.productTitle > a')
        prices = soup.select('p.productPrice > em')
        shops = soup.select('.productShop > a')
        sell_nums = soup.select('.productStatus > span > em')
        talk_nums = soup.select('.productStatus > span > a')
        for title,price,shop,sell_num,talk_num in zip(titles,prices,shops,sell_nums,talk_nums):
            data = {
                'title':title.get_text(),
                'price':price.get_text(),
                'shop':shop.get_text(),
                'sell_num':sell_num.get_text(),
                'talk_num':talk_num.get_text()
            }
            print(data)
            sheet_tab_1.insert_one(data)

# get_info()
for item in sheet_tab_1.find():
    print(item)





















