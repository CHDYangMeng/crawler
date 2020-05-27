from crawler import get_information
import time


def get_urls():
    # for i in range(start, end, 1):
    urls = 'http://www.dianping.com/search/keyword/17/0_火锅'
    time.sleep(2)
    get_information(urls)
