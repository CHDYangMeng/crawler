
from bs4 import BeautifulSoup
import requests
import re

from numpy import unicode

url = 'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.text, 'lxml')
tables = soup.select('#content_right > div.overflow > table > tbody')
print(tables)


# ulist = []
# for tr in tables:
#     ui = []
#     for td in tr:
#         ui.append(td.href)
#         print(ui)
#     ulist.append(ui)
