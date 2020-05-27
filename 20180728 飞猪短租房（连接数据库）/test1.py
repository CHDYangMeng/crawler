import pymysql

def connect_sql():
    try:
        conn = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = 'test',
            charset = 'utf8'
        )
    except Exception as e:
        print(e)
    else:
        print('连接成功')
        conn_cur = conn.cursor()
        return conn_cur,conn

def create_tab(Tablename,data):
    COLstr = ''
    ROWstr = ''
    sql_key = ''
    ColumnStyle = 'VARCHAR(20)'
    for key in data.keys():
        COLstr = COLstr + key + ' ' + ColumnStyle + ','
        ROWstr = (ROWstr + '"%s"' + ',')%(data[key])
        sql_key = sql_key + '' + key + ','
    print(COLstr[:-1])
    print(ROWstr[:-1])
    print(sql_key[:-1])

    try:
        connect_sql()[0].execute("SELECT * FROM %s"%(Tablename))
        connect_sql()[0].execute("INSERT INTO %s(%s) VALUES (%s)"%(Tablename,sql_key[:-1],ROWstr[:-1]))
        print('1')
    except Exception as e:
        connect_sql()[0].execute("CREATE TABLE %s(%s)"%(Tablename,COLstr[:-1]))
        connect_sql()[0].execute("INSERT INTO %s(%s) VALUES (%s)"%(Tablename,sql_key[:-1],ROWstr[:-1]))
        print('2')
    connect_sql()[1].commit()
    connect_sql()[0].close()
    connect_sql()[1].close()

data = {
    'id': 0o01,
    'name': 'zhangsan',
    'sex': 'men',
    'score': 98
}

create_tab('test',data)