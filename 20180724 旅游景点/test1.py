
from bs4 import BeautifulSoup
import requests
import time
import warnings
warnings.filterwarnings("ignore")

url = 'https://www.tripadvisor.cn/Attractions-g60763-Activities-New_York_City_New_York.html'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text,'lxml')
# print(soup)
titles = soup.select('.poiTitle')
talks = soup.select('.review_count')
images = soup.select('img[width="200"]')
descriptions = soup.select('div.item')
# print(titles[0].get_text())
# print(talks[0].get_text())
# print(image[0].get('src'))
# print(description[2].get_text())
des = []
i = 2
flag = 0
while(i<=240):
    # print(descriptions[i].get_text())
    des.append(descriptions[i].get_text())
    i = i + 4
# print(des)
#     flag = flag + 1
# print(flag)
# for title in titles:
#     print(title.get_text())

for title,image,talk,description in zip(titles,images,talks,des):
    data = {
        'title':title.get_text(),
        'image':image.get('src'),
        'talk':talk.get_text(),
        'description':description
    }
    print(data)













