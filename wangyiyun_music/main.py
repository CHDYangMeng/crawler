
from bs4 import BeautifulSoup
import requests

url = 'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=月光'
headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

response = requests.get(url,headers=headers)
soup = BeautifulSoup(response.text,'lxml')
print(soup)
