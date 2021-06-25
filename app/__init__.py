# -*- coding = utf-8 -*-
# @Time : 2021/6/24 15:08
# @File : __init__.py.py
# @Software: PyCharm

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = "login"
login.login_message = u"你要登录才能访问此页面."
login.login_message_category = "info"

from app.routes import *
