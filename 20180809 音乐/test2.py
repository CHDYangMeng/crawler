
import requests
import json
import re
from bs4 import BeautifulSoup

def get_keyword(songmid,songname):
    url_express = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=2066708427&jsonpCallback=MusicJsonCallback8887430003644365&loginUin=603894673&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback8887430003644365&uin=603894673&songmid='+songmid+'&filename=C400'+songmid+'.m4a&guid=1319365062'
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url_express,headers = headers)
    concent = response.content.decode()
    json_data = re.compile(r"{.*}")
    json_data = json_data.search(concent).group()
    json_file = json.loads(json_data)
    flag_data = json_file.get('data').get('items')
    filename = flag_data[0]['filename']
    songmid = flag_data[0]['songmid']
    vkey = flag_data[0]['vkey']
    get_music(filename,songmid,vkey,songname)


def get_music(filename,songmid,vkey,songname):
    url_music = 'http://dl.stream.qqmusic.qq.com/'+filename+'?vkey='+vkey+'&guid=1319365062&uin=603894673&fromtag=66'
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url_music,headers = headers)
    concent = response.content
    download(songname,concent)

def download(songname,content):
    path = 'E:\\crawler\\20180809_auto\Music\\'+songname+'.mp3'
    with open(path ,'wb') as f:
        f.write(content)
        f.close()
        print('downloading:'+songname+'.mp3')

def get_song_link():
    page = get_num()
    for i in range(1,page):
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=1090854909&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=603894673&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid=002J4UUk29y8BY&order=listen&begin='+str(i*30)+'&num=30&songstatus=1'
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        response = requests.get(url,headers = headers)
        concent = response.content.decode()
        json_data = re.compile(r"{.*}")
        json_data = json_data.search(concent).group()
        json_file = json.loads(json_data)
        file_datas = json_file.get('data').get('list')
        for file_data in file_datas:
            songmid = file_data['musicData']['songmid']
            songname = file_data['musicData']['songname']
            get_keyword(songmid,songname)

def get_num():
    url = 'https://y.qq.com/n/yqq/singer/002J4UUk29y8BY.html#tab=song&stat=y_new.singerlist.singerpic'
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    num = soup.select('strong.data_statistic__number')[0].get_text()
    num = int(num)
    page = int(num/30)
    if (page%30) == 0:
        return page
    else:
        return page + 1

if __name__=='__main__':
    get_song_link()



























































