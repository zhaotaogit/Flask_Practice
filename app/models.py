# -*- coding = utf-8 -*-
# @Time : 2021/6/24 18:37
# @File : models.py
# @Software: PyCharm
from app import db
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'User: {self.username}'


# 书号，书名，类别，作者，出版社，价格，库存量

class Book(db.Model, UserMixin):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    # img = db.Column(db.String(64),nullable=False)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    author = db.Column(db.String(64), nullable=False)
    # 出版社
    provenance = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float,nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'User: {self.name}'
