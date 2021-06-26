# -*- coding = utf-8 -*-
# @Time : 2021/6/24 16:03
# @File : func.py
# @Software: PyCharm
import sqlite3
import os


def add_user(username, password, email):
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    sql = f"insert into User(username,password,email) values('{username}','{password}','{email}')"
    curs.execute(sql)
    curs.close()
    conn.commit()


def search_user(username):
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    sql = f"select username from User where username = '{username}'"
    print(sql)
    result = curs.execute(sql).fetchone()
    curs.close()
    conn.close()
    print(result)
    return result


def is_pwd_true(username, password):
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    sql = f"select password from User where username = '{username}'"
    print(sql)
    result = curs.execute(sql).fetchone()
    curs.close()
    conn.close()
    print(result)
    if password != result[0]:
        return False
    return True


def search_email(email):
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    sql = f"select email from User where email = '{email}'"
    print(sql)
    result = curs.execute(sql).fetchone()
    curs.close()
    conn.close()
    print(result)
    return result


# 定义添加书籍函数


