from bs4 import BeautifulSoup
import requests
import time
import warnings
warnings.filterwarnings("ignore")

urls = ['https://www.tripadvisor.cn/Attractions-g60763-Activities-oa30-zfn7102352-New_York_City_New_York.html#FILTERED_LIST'.format(str(i)) for i in range(30, 330, 30)]
# url = 'https://www.tripadvisor.cn/Attractions-g60763-Activities-zfn7102352-New_York_City_New_York.html'

def get_info(url,data=None):
    we_web = requests.get(url)
    soup = BeautifulSoup(we_web.text, 'lxml')
    titles = soup.select('div.listing_title > a')
    talks = soup.select('span.more > a')
    description = soup.select('div.p13n_reasoning_v2')
    for title, talk, des in zip(titles, talks, description):
        data = {
            'title': title.get_text(),
            'talk': talk.get_text().strip(),
            'des': list(des.stripped_strings)
        }
        print(data)
for single_url in urls:
    get_info(single_url)

