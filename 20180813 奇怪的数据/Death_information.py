
from bs4 import BeautifulSoup
import requests
import pandas

def get_table(ulist):

    url = 'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url,headers)
    soup = BeautifulSoup(response.text,'lxml')
    trs = soup.find_all('tr')
    for tr in trs:
        ui = []
        for td in tr:
            ui.append(td.string)
        ulist.append(ui)
    download(ulist)

def download(ulist):
    pandas.DataFrame(ulist).to_excel("Death_information.xlsx", sheet_name="Death_information", index=False, header=True)

if __name__=='__main__':
    ulist = []
    get_table(ulist)