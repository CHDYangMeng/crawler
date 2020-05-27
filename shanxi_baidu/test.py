import requests
import time

# 104.166102,31.707044
# 111.469829,39.763705

# 108.880409,34.220028
# 108.912245,34.234057
url = 'http://api.map.baidu.com/place/v2/search?query=交通设施&tag=收费站&region=233&output=json&ak=4wAjx3T4AQtpbqfwuNByB83XkWWVhN0o'
response = requests.get(url)
soup = response.json()
# names = soup['results'][0]['name']
# lat = soup['results']['location'][0]
# lon = soup['results']['location'][1]
print(soup)