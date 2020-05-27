
import requests
import base64
import os
import json
import time

def get_img_base(file):
    with open(file, 'rb') as fp:
        content = base64.b64encode(fp.read())
        return content

file_path = 'F:/python_爬虫/zhuhu_nv/picture'
file_path_photo = 'F:/python_爬虫/zhuhu_nv/photo'
list_paths = os.listdir(file_path)

for list_path in list_paths:
    img_path = file_path + '/' + list_path
    token = '24.afb99efee5b78e29acc74302ecf56ef7.2592000.1554554800.282335-15707843'
    request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    request_url_fin = request_url + '?access_token=' + token
    params = {
        'image': get_img_base(img_path),
        'image_type': 'BASE64',
        'face_field': 'age,beauty,gender'
    }

    res = requests.post(request_url_fin, data=params)
    json_result = json.loads(res.text)
    code = json_result['error_code']

    if code == 222202:
        continue
    try:
        gender = json_result['result']['face_list'][0]['gender']['type']
        if gender == 'male':
            continue
        beauty = json_result['result']['face_list'][0]['beauty']
        new_beauty = round(beauty/10,1)
        print(img_path,new_beauty)
        if new_beauty >= 8:
            os.rename(os.path.join(file_path, list_path), os.path.join(file_path_photo,'8分',str(new_beauty) + '_' + list_path))
        elif new_beauty >= 7:
            os.rename(os.path.join(file_path, list_path), os.path.join(file_path_photo,'7分', str(new_beauty) + '_' + list_path))
        elif new_beauty >= 6:
            os.rename(os.path.join(file_path, list_path), os.path.join(file_path_photo,'6分', str(new_beauty) + '_' + list_path))
        elif new_beauty >= 5:
            os.rename(os.path.join(file_path, list_path), os.path.join(file_path_photo,'5分', str(new_beauty) + '_' + list_path))
        else:
            os.rename(os.path.join(file_path, list_path), os.path.join(file_path_photo,'其他分数', str(new_beauty) + '_' + list_path))
        time.time(2)
    except KeyError:
        pass
    except TypeError:
        pass