from flask import render_template, flash, redirect, url_for, session, request

from app import app, db
from app.forms import RegisterForm, LoginForm, RetrievePasswordForm, SelectBookForm, AddBookForm
from app.models import User, Book
# from app.func import add_user, search_user, is_pwd_true, search_email, add_book
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('index.html', name=session.get('username'))
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()  # 判断用户是否才存在
        if user and password == user.password:
            # session['username'] = username
            print(user.password)
            print(user, password)
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        # print(username)
        email = form.email.data
        user = User.query.filter_by(username=username).first()  # 判断用户是否存在
        email = User.query.filter_by(email=email).first()
        if user or email:
            flash("用户名或邮箱已存在!")
        else:
            try:
                password = form.password.data
                user = User(username=username, email=form.email.data, password=password)
                db.session.add(user)
                db.session.commit()
                flash("注册成功", 'info')
                return redirect(url_for('register'))
            except Exception as e:
                db.session.rollback()
                flash("注册失败", category='info')
                print(e)
    return render_template('register.html', form=form)


@app.route('/retrieve_password/', methods=['GET', 'POST'])
def retrieve_password():
    form = RetrievePasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            pass
        else:
            flash("邮箱不存在!", category='info')
    return render_template('retrieve_password.html', form=form)


@app.route('/admin/')
def admin():
    print(request.endpoint)
    return render_template('admin.html')


@app.route('/admin/select_book/<int:page>', methods=['GET', 'POST'])
def select_book(page):
    if not page or page < 1:
        page = 1
    form = SelectBookForm()
    if form.validate_on_submit():
        print(form.select.data)
        return redirect(url_for('select_book', page=1))
        # 分页器对象
    table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10,
                                                           error_out=True)

    # print(request.endpoint)
    return render_template('select_book.html', form=form, table_page=table_paginate)


# 浏览书籍信息路由
@app.route('/admin/look_book/<int:page>', methods=['GET', 'POST'])
def look_book(page):
    if not page or page < 1:
        page = 1
    table = Book.query.all()
    form = AddBookForm()
    # 分页器对象
    table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10,
                                                           error_out=True)  # page代表那一页。每页显示2个，超出页数显示空列表
    # print('debug')
    # print(table_paginate)
    # print(table_paginate.pages) # 一共多少页
    # print(table_paginate.has_next)  # 是否有下一页
    # print(table_paginate.has_prev)  # 是否有上一页
    # print(table_paginate.next_num)  # 下一页页码
    # print(table_paginate.prev_num)  # 上一页页码
    if request.method == 'POST':
        if form.validate_on_submit:
            print('debug')
            # 获取表单数据
            book_id = form.id.data
            book_name = form.name.data
            book_category = form.category.data
            book_author = form.author.data
            book_provenance = form.provenance.data
            book_price = form.price.data
            book_num = form.num.data
            print(book_id, book_name, book_category, book_author, book_provenance, book_price, book_num)
            obj_book_id = Book.query.filter_by(id=book_id).first()
            if obj_book_id:  # 判断书籍编号是否存在，书籍编号不可重复
                if obj_book_id.name == book_name and obj_book_id.category == book_category and obj_book_id.author == book_author:
                    if obj_book_id.provenance == book_provenance and obj_book_id.price == book_price:
                        obj_book_id.count += int(book_num)
                        db.session.commit()
                        flash("添加成功！", category='info')
                else:
                    flash("添加失败,书籍编号已存在!")
            else:
                add_book(book_id=book_id, book_name=book_name, book_category=book_category,
                         book_author=book_author,
                         book_provenance=book_provenance, book_price=book_price, book_num=book_num)
    return render_template('look_book.html', table=table, table_page=table_paginate, form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))


def add_book(book_id, book_name, book_category, book_author, book_provenance, book_price, book_num):
    try:
        book = Book(id=book_id, name=book_name, category=book_category,
                    author=book_author,
                    provenance=book_provenance, price=book_price, count=book_num)
        db.session.add(book)
        db.session.commit()
        flash('书籍添加成功！', category='info')
        print('添加成功')
        return redirect(url_for('look_book', page=1))
    except Exception as e:
        db.session.rollback()
        print(e)
        print('添加失败！')
        flash("书籍添加失败!", category='info')
        return redirect(url_for('look_book', page=1))
