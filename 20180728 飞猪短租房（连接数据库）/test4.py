
from test3 import DataToMysql

mysql = DataToMysql('localhost','root','root','test')
di = {"A": "A", "B": "B"}
mysql.write('te', di)





























