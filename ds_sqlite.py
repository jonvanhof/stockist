import sqlite3


class ds_sqlite:
    def __init__(self, dbname):
        self.cn = sqlite3.connect(dbname + '.db')
        self.cr = self.cn.cursor()


