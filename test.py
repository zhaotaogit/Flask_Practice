# -*- coding = utf-8 -*-
# @Time : 2021/6/24 16:13
# @File : test.py
# @Software: PyCharm
import sqlite3

username = '1787417712'

conn = sqlite3.connect('data.db')
# conn.row_factory = sqlite3.Row
curs = conn.cursor()
sql = f"select username,password from User where username = '{username}'"
# print(sql)
result = curs.execute(sql).fetchone()
curs.close()
conn.close()
print(result[1])
# for i in result:
#     print(i)


