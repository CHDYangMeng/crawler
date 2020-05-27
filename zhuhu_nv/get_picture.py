
import requests
import json
import time
import re

headers = {
    'user-agent' :
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'cookie' :
        '_zap=8889b707-0a96-4c2e-bdf2-355baca2f639; d_c0="AGDoOj_xXw6PTqWj_6YFXJ0wSGb_8ltGj4g=|1539736752"; __gads=ID=0185d5439576213f:T=1539736780:S=ALNI_MY2mMtHHmPH8Eb0u9OyjMoAFx0SBw; tst=r; __utmv=51854390.100--|2=registration_date=20161007=1^3=entry_date=20161007=1; _xsrf=GUDFSgPqRsODuW6bwFYsU5VW05kMFXXl; __utma=51854390.141516793.1545222870.1545222870.1547450073.2; __utmz=51854390.1547450073.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/23615530/answer/25154094; q_c1=15dc7dd85b9c4252a3ce7951e2c2df7e|1551947224000|1539736778000; capsion_ticket="2|1:0|10:1551947470|14:capsion_ticket|44:ZWI5MmUzNjYyMmIzNGNjMGE4Y2RiMzQ3YTFmOTZmNzg=|f9e4fd2658f81cfe5475fded88fe76ab6b924301b28a52665b4fbe36f5df5820"; tgw_l7_route=e5fff8427ab0da864ad8c176457be0a7'
}

def get_img(url):
    res = requests.get(url, headers=headers)
    i = 1
    json_data = json.loads(res.text)
    datas = json_data['data']
    for data in datas:
        id = data['author']['name']
        content = data['content']
        imgs = re.findall('img src="(.*?)"', content, re.S)
        if len(imgs) == 0:
            pass
        else:
            for img in imgs:
                if 'jpg' in img:
                    res_1 = requests.get(img, headers=headers)
                    fp = open('F:/python_爬虫/zhuhu_nv/picture/' + id + '+' + str(i) + '.jpg', 'wb')
                    fp.write(res_1.content)
                    i = i + 1
                    print(id, img)

if __name__ == '__main__':
    for i in range(0, 2500, 5):
        url = 'https://www.zhihu.com/api/v4/questions/29024583/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset='+ str(i) +'&platform=desktop&sort_by=default'
        get_img(url)
        time.sleep(3)
