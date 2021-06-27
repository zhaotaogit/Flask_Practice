# -*- coding = utf-8 -*-
# @Time : 2021/6/24 18:51
# @File : config.py
# @Software: PyCharm
import os

path = os.getcwd()

class Config:
    WTF_CSRF_ENABLED = False
    # CSRF_ENABLED = True
    # CSRF = 'CSRF'
    SECRET_KEY = 'long SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(path, 'data.db')
                              # 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False