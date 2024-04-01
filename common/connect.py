from common.recordlog import logs
from conf.oprateConfig import OprateConfig
import pymysql

conf = OprateConfig()


class ConnectMysql:
    def __init__(self):
        mysql_conf = {
            "host": conf.get_mysql("host"),
            "port": int(conf.get_mysql("port")),
            "user": conf.get_mysql("username"),
            "password": conf.get_mysql("password"),
            "database": conf.get_mysql("database"),
        }
        try:
            self.conn = pymysql.connect(**mysql_conf, charset="utf8")  # 读取配置字典
            # print(self.conn)
            # pymysql.cursors.DictCursor数据库以键值对的方式显示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("成功连mysql host:{host} port{port} db{database}".format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()


if __name__ == '__main__':
    conn = ConnectMysql()
    sql = "select * from books"
    print(conn.query(sql))
