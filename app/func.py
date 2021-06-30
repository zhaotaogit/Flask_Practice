# -*- coding = utf-8 -*-
# @Time : 2021/6/24 16:03
# @File : func.py
# @Software: PyCharm
# import sqlite3
# import os


import smtplib
from email.mime.text import MIMEText
import random



def send_mail(receivers):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'zhaotaotao920'
    # 密码(部分邮箱为授权码)
    mail_pass = 'ZLFIMYLDFVBQRLEI'
    # 邮件发送方邮箱地址
    sender = 'zhaotaotao920@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [f'{receivers}']
    verification_code = random.randint(100000,999999)
    # 设置email信息
    # 邮件内容设置
    message = MIMEText(f'验证码为：{verification_code}', 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '重置密码'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    for i in receivers:
        message['To'] = i

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        print('success')
        return True,verification_code
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误
        return False










#
#
#
#
#
#
# def add_user(username, password, email):
#     conn = sqlite3.connect('data.db')
#     conn.row_factory = sqlite3.Row
#     curs = conn.cursor()
#     sql = f"insert into User(username,password,email) values('{username}','{password}','{email}')"
#     curs.execute(sql)
#     curs.close()
#     conn.commit()
#
#
# def search_user(username):
#     conn = sqlite3.connect('data.db')
#     conn.row_factory = sqlite3.Row
#     curs = conn.cursor()
#     sql = f"select username from User where username = '{username}'"
#     print(sql)
#     result = curs.execute(sql).fetchone()
#     curs.close()
#     conn.close()
#     print(result)
#     return result
#
#
# def is_pwd_true(username, password):
#     conn = sqlite3.connect('data.db')
#     curs = conn.cursor()
#     sql = f"select password from User where username = '{username}'"
#     print(sql)
#     result = curs.execute(sql).fetchone()
#     curs.close()
#     conn.close()
#     print(result)
#     if password != result[0]:
#         return False
#     return True
#
#
# def search_email(email):
#     conn = sqlite3.connect('data.db')
#     conn.row_factory = sqlite3.Row
#     curs = conn.cursor()
#     sql = f"select email from User where email = '{email}'"
#     print(sql)
#     result = curs.execute(sql).fetchone()
#     curs.close()
#     conn.close()
#     print(result)
#     return result
#
#
# # 定义添加书籍函数
#
#
