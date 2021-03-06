import pymysql

class DataToMysql:
    def __init__(self, host, user, passwd, db):
        try:
            self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db,
                                        port=3306, charset='utf8')  # 链接数据库
            self.cursor = self.conn.cursor()
        except pymysql.Error as e:
            print("数据库连接信息报错")
            raise e

    def write(self, table_name, info_dict):
        """
        根据table_name与info自动生成建表语句和insert插入语句
        :param table_name: 数据需要写入的表名
        :param info_dict: 需要写入的内容，类型为字典
        :return:
        """
        sql_key = ''  # 数据库行字段
        sql_value = ''  # 数据库值
        for key in info_dict.keys():  # 生成insert插入语句
            sql_value = (sql_value + '"' + pymysql.escape_string(info_dict[key]) + '"' + ',')
            sql_key = sql_key + ' ' + key + ','

        try:
            self.cursor.execute(
                "INSERT INTO %s (%s) VALUES (%s)" % (table_name, sql_key[:-1], sql_value[:-1]))
            self.conn.commit()  # 提交当前事务
        except pymysql.Error as e:
            if str(e).split(',')[0].split('(')[1] == "1146":  # 当表不存在时，生成建表语句并建表
                sql_key_str = ''  # 用于数据库创建语句
                columnStyle = ' text'  # 数据库字段类型
                for key in info_dict.keys():
                    sql_key_str = sql_key_str + ' ' + key + columnStyle + ','
                self.cursor.execute("CREATE TABLE %s (%s)" % (table_name, sql_key_str[:-1]))
                self.cursor.execute("INSERT INTO %s (%s) VALUES (%s)" %
                                    (table_name, sql_key[:-1], sql_value[:-1]))
                self.conn.commit()  # 提交当前事务
            else:
                raise
