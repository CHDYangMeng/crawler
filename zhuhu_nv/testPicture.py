
import requests
import base64
import json



def get_img_base(file):
    with open(file,'rb') as fp:
        content = base64.b64encode(fp.read())
        return content

def get_result(images):
    img_path = 'F:/python_爬虫/zhuhu_nv/test/' + images
    request_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
    request_url_finllay = request_url + '?access_token=' + token

    params = {
        'image': get_img_base(img_path),
        'image_type': 'BASE64',
        'face_field': 'age,beauty,gender'
    }
    res = requests.get(request_url_finllay, data=params)
    json_result = json.loads(res.text)
    print(json_result)
    code = json_result['error_code']
    gender = json_result['result']['face_list'][0]['gender']['type']
    beauty = json_result['result']['face_list'][0]['beauty']
    print(code, gender, beauty)

if __name__ == '__main__':
    image = '20190510222716.jpg'
    token = '24.69175eaee343f59d676b21a874f4cbc3.2592000.1560093474.282335-16223824'
    get_result(image)
