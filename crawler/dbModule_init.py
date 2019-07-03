import pymysql

# mysql db connection
class Mysql:
    def __init__(self):
        self.db = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='password',
                    db='db',
                    charset='utf8')
        self.cursor = self.db.cursor()

    def execute(self, sql, params = None):
        self.cursor.execute(sql, params)

    def query(self, sql, params = None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def commit(self):
        self.db.commit()
