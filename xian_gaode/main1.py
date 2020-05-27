
import requests
import time
import pandas
import datetime
'''
左下坐标：108.857217,34.203641
右上坐标：109.024759,34.334437
'''
def get_station(left_lat,left_lon,right_lat,right_lon,df):
    flag1 = 1
    if((right_lat-left_lat > 0.05) & (right_lon-left_lon > 0.05)):
        while(right_lon > left_lon):
            left_lat_t = left_lat
            flag2 = 0
            while(right_lat > left_lat_t):
                right_lat_new = left_lat_t + 0.05
                right_lon_new = left_lon + 0.05
                left_lat_str = str(left_lat_t)
                left_lon_str = str(left_lon)
                right_lat_str = str(right_lat_new)
                right_lon_str = str(right_lon_new)
                df = get_data(left_lat_str, left_lon_str, right_lat_str, right_lon_str)
                df = df.append(df)
                left_lat_t = right_lat_new
                time.sleep(5)
                flag2 = flag2 + 1
                print("爬起第"+str(flag1)+"行"+",第"+str(flag2)+"列")
            left_lon = left_lon + 0.05
            flag1 = flag1 + 1
    else:
        left_lat_str = str(left_lat)
        left_lon_str = str(left_lon)
        right_lat_str = str(right_lat)
        right_lon_str = str(right_lon)
        df = get_data(left_lat_str, left_lon_str, right_lat_str, right_lon_str)
    pandas.DataFrame(df).to_excel("TrafficStatus.xlsx", sheet_name="TrafficStatus", index=False, header=True)

def get_data(left_lat,left_lon,right_lat,right_lon):

    headers = {
        
    }
    url = 'https://restapi.amap.com/v3/traffic/status/rectangle?rectangle='+left_lat+','+left_lon+';'+right_lat+','+right_lon+'&key=b3f27946ff767f3e953b29fbe061202d&extensions=all'
    json_obj = requests.get(url)
    data = json_obj.json()
    print(data['info'])
    # # time.sleep(2)
    df = pandas.DataFrame()
    for road in data['trafficinfo']['roads']:
        rname = road['name']
        rstatus = road['status']
        rdirection = road['direction']
        try:
            rspeed = road['speed']
        except:
            rspeed = 0
        rangle = road['angle']
        rployline = road['polyline'].split(';')

        for i in range(0, len(rployline)):
            data = {
                '0time': datetime.datetime.now(),
                '1rname': rname,
                '2rdirection': rdirection,
                '3rstatus': rstatus,
                '4rspeed': rspeed,
                '5angle': rangle,
                '6rployline': rployline[i],
                '7detail direction': rname + '-' + rdirection
            }
            print(df)
            df = df.append(data, ignore_index=True)
    return df
    # pandas.DataFrame(df).to_excel("TrafficStatus.xlsx", sheet_name="TrafficStatus", index=False, header=True)

if __name__ == '__main__':
    print("开始爬取数据!")
    start_time = time.time()
    df = pandas.DataFrame()
    get_station(108.857217,34.203641,109.024759,34.334437,df)
    end_time = time.time()
    print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))







