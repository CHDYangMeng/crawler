
from bs4 import BeautifulSoup
import requests
import time
import re
import json
import pandas


def get_link_and_information():
    url = 'http://apps.game.qq.com/lol/act/a20160519Match/Match.php?_a=teamsearch&iGameId=95&sGameType=7,8&iPage=1&sRet=TEAMRANKLIST&r=0.15970827546490174&_=1534166357723'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    concent = response.content.decode()
    json_data = re.compile(r"{.*}")
    json_data = json_data.search(concent).group()
    json_file = json.loads(json_data)
    file_datas = json_file.get('msg').get('data')
    df = pandas.DataFrame()
    for file_data in file_datas:
        teamname =  file_data['sTeamName']
        win = file_data['iWin']
        loss = file_data['iLoss']
        kill = file_data['iKill']
        death = file_data['iDeath']
        Winrate = file_data['sAveragingWin']
        Avekill = file_data['sAveragingKill']
        Avedeath = file_data['sAveragingDeath']
        Avegold = file_data['sAveragingGold']
        Avesmalldragon = file_data['sAveragingSmallDragon']
        Avebigdragon = file_data['sAveragingBigDragon']
        data = {
            'teamname':teamname,
            'win':win,
            'loss':loss,
            'kill':kill,
            'death':death,
            'Winrate':Winrate,
            'Avekill':Avekill,
            'Avedeath':Avedeath,
            'Avegold':Avegold,
            'Avesmalldragon':Avesmalldragon,
            'Avebigdragon':Avebigdragon
        }
        print(data)
        df = df.append(data,ignore_index=True)
    pandas.DataFrame(df).to_excel("abc.xlsx", sheet_name="123", index=False, header=True)

if __name__=='__main__':
    get_link_and_information()