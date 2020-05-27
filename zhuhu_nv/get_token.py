
'''
token每30天换一次
'''
import urllib

import requests

ak = 'S8xemEonUSqW9A2pNX5xyFqo'
sk = 'fGh3GMD1bpMVb5tyOiVfEtG0YDoWT3Bt'

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(ak, sk)
# res = requests.post(host)
# print(res.text)

# client_id 为官网获取的AK， client_secret 为官网获取的SK，以下一行按自己实际填写
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(type(content))#<class 'bytes'>
content_str=str(content, encoding="utf-8")
###eval将字符串转换成字典
content_dir = eval(content_str)
access_token = content_dir['access_token']
print(access_token)