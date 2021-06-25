# -*- coding = utf-8 -*-
# @Time : 2021/6/24 18:51
# @File : config.py
# @Software: PyCharm
import os

path = os.getcwd()

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'long SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'data.db')
                              # 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False