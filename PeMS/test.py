
# times = '01/03/2018 00:00'
# t1 = times.split(' ')
# date = t1[0]
# t2 = date.split('/')
# year = t2[2]
# month = t2[0]
# day = t2[1]
# time = t1[1]
#
# t_fin = year + '-' + month + '-' + day + ' ' + time + ':00'
#
# print(t_fin)

str = '22.33'
print(float(str))


station_ids = [
        '400075', '400093', '400203', '400218', '400242', '400300', '400400', '400454', '400480', '400489',
        '400606', '400609', '400642', '400655', '400659', '400765', '400815', '400835', '400844', '400923',
        '400980', '400983', '401137', '401141', '401142', '401143', '401144', '401156', '401190', '401273',
        '401333', '401339', '401390', '401413', '401416', '401471', '401478', '401481', '401539', '401562',
        '401610', '401615', '401657', '401671', '401698', '401708', '401714', '401896', '401898', '401899',
        '401911', '403280', '403430', '404746', '404761', '405450', '408138'
    ]

t = '1153.0'

t1 = t.split(',')[0]
t2 = t.split(',')[1]
print(t1)
print(t2)