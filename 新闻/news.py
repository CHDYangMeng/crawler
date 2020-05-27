
import json
import re
import requests

def get_link():
    url = 'https://www.toutiao.com/api/pc/feed/?category=news_military&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A185BB8766B8C95&cp=5B76F8BCF9951E1&_signature=s8r1DQAA6MpSYGCnOShDdbPK9R'
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    connect = response.content.decode()
    json_data = re.compile(r"{.*}")
    json_data = json_data.search(connect).group()
    json_file = json.loads(json_data)
    file = json_file.get('data')
    print(file)

if __name__ == '__main__':
    get_link()


























