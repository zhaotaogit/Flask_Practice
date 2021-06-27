# -*- coding = utf-8 -*-
# @Time : 2021/6/24 15:08
# @File : __init__.py.py
# @Software: PyCharm

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager
# from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
bootstrap = Bootstrap(app)

# 先导入config，再创建实例不然会有提示
app.config.from_object(Config)
db = SQLAlchemy(app)
# csrf = CsrfProtect(app)
login = LoginManager(app)
login.login_view = "login"
login.login_message = u"你要登录才能访问此页面."
login.login_message_category = "info"

from app.routes import *
