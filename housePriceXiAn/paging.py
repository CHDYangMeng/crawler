from crawler import get_information
import time

def get_urls(start,end):
    for i in range(start,end,1):
        urls = 'https://xa.fang.ke.com/loupan/pg{}/'.format(str(i))
        time.sleep(2)
        get_information(urls)