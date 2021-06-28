from flask import render_template, flash, redirect, url_for, session, request

from app import app, db
from app.forms import RegisterForm, LoginForm, RetrievePasswordForm, SelectBookForm, AddBookForm, DelBookForm
from app.models import User, Book
# from app.func import add_user, search_user, is_pwd_true, search_email, add_book
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
@login_required
def home():
    print(current_user.username)
    # if not page or page < 1:
    #     page = 1
    # table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10, error_out=True)
    return render_template('index.html', name=current_user.username, title='首页')

@app.route('/personal_center')
@login_required
def personal_center():
    return render_template('personal_center.html')


@app.route('/bookinfo/<int:page>')
@login_required
def bookinfo(page):
    if not page or page < 1:
        page = 1
    table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10, error_out=True)
    return render_template('bookinfo.html', table_page=table_paginate)


@app.route('/buybook/', methods=['GET', 'POST'])
@login_required
def buybook():
    if request.method == 'GET':
        book_id = request.args.get('book_id')
        if not book_id:
            return render_template('buybook.html')
        book = Book.query.filter_by(id=book_id).first()
        return render_template('buybook.html',book=book)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        num = form_data.get('num')
        print(form_data)
        print(num)
        book_id = form_data.get('book_id')
        if not book_id:
            flash("你还没有选择要购买的书!",category='info')
            print('你还没有选择要购买的书！')
            return redirect(url_for('buybook'))
        else:
            book = Book.query.filter_by(id=book_id).first()
            book_num = book.count
            if book_num > int(num):
                book.count -= int(num)
                db.session.commit()
                flash("购买成功!",category='info')
                print('购买成功！')
                return redirect(url_for('buybook',book_id=book_id))
            else:
                flash("库存不足,请联系管理员!",category='info')
                print('库存不足,请联系管理员!')
                return redirect(url_for('buybook', book_id=book_id))
    return redirect(url_for('buybook'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()  # 判断用户是否才存在
        if user:
            if password == user.password:
                # session['username'] = username
                print(user.password)
                print(user, password)
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            else:
                flash('用户名或密码错误!',category='info')
        else:
            flash("登录的用户不存在!",category='info')
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
                user = User(username=username, password=password, email=form.email.data, )
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


# @app.route('/admin/')
# @login_required
# def admin():
#     print(request.endpoint)
#     return render_template('admin.html')


@app.route('/admin/select_book/<int:page>', methods=['GET', 'POST'])
@login_required
def select_book(page):
    if not page or page < 1:
        page = 1
    form = SelectBookForm()
    alter_form = AddBookForm()
    remove_form = DelBookForm()
    # 分页器对象
    table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10, error_out=True)
    if form.validate_on_submit():
        print('debug:点击1')
        print(form.select.data)
        number = form.select.data
        text = form.text.data
        try:
            table_paginate = selectbook(number, text, page)
        except Exception as e:
            print(e)
            flash("查询失败,请重试!", category='info')
        if form.operatin_select.data == 2:
            print('debug:修改操作，获取值:', form.operatin_select.data)
            return render_template('select_book.html', alter_form=alter_form, table_page=table_paginate)
        elif form.operatin_select.data == 3:
            print('debug:修改操作，获取值:', form.operatin_select.data)
            remove_form = AddBookForm()
            return render_template('select_book.html', remove_form=remove_form, table_page=table_paginate)
    # 修改书籍信息
    if alter_form.validate_on_submit():
        print('debug:测试点击2')
        print(alter_form.bool.data)
        if alter_form.bool.data:
            book_id = alter_form.id.data
            book_name = alter_form.name.data
            book_category = alter_form.category.data
            book_author = alter_form.author.data
            book_provenance = alter_form.provenance.data
            book_price = alter_form.price.data
            book_num = alter_form.num.data
            # 判断要修改的书籍是否存在
            book = Book.query.filter_by(id=book_id).first()
            if book:
                try:
                    book.name = book_name
                    book.category = book_category
                    book.author = book_author
                    book.provenance = book_provenance
                    book.price = book_price
                    book.count = book_num
                    db.session.commit()
                    flash('书籍修改成功！', category='info')
                    print('修改成功')
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    print('修改失败！')
                    flash("书籍修改失败，请重试!", category='info')
                    # return render_template('select_book.html', alter_form=alter_form, table_page=table_paginate)
            else:
                flash("要修改的书籍不存在！", category="info")
        else:
            flash("请确认要修改的信息！")
        return render_template('select_book.html', alter_form=alter_form, table_page=table_paginate)
    if remove_form.validate_on_submit():
        print('测试删除3')
        id = remove_form.id.data
        if not remove_form.bool.data:
            flash("请确认要删除的信息！", category='info')
            return render_template('select_book.html', remove_form=remove_form, table_page=table_paginate)
        else:
            book = Book.query.filter_by(id=id).first()
            if book:
                Book.query.filter_by(id=id).delete()
                db.session.commit()
                flash("删除成功！", category='info')
                # return redirect(url_for('select_book',page=page))
                table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10, error_out=True)
                return render_template('select_book.html', remove_form=remove_form, table_page=table_paginate)
            else:
                flash("输入的书籍编号不存在!", category='info')
            return render_template('select_book.html', remove_form=remove_form, table_page=table_paginate)
    # print(request.endpoint)
    return render_template('select_book.html', form=form, table_page=table_paginate)


# 浏览书籍信息路由
@app.route('/admin/look_book/<int:page>', methods=['GET', 'POST'])
@login_required
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
@login_required
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


def selectbook(number, text, page):
    if number == 1:
        table = Book.query.filter_by(id=text).order_by(Book.id)
        count = table.count()
        print('debug数量', count)
        table_paginate = table.paginate(page, per_page=10, error_out=True)
    elif number == 2:
        table = Book.query.filter_by(name=text).order_by(Book.id)
        count = table.count()
        print('debug数量', count)
        table_paginate = table.paginate(page, per_page=10, error_out=True)
    elif number == 3:
        table = Book.query.filter_by(category=text).order_by(Book.id)
        count = table.count()
        print('debug数量', count)
        table_paginate = table.paginate(page, per_page=10, error_out=True)
    elif number == 4:
        table = Book.query.filter_by(author=text).order_by(Book.id)
        count = table.count()
        print('debug数量', count)
        table_paginate = table.paginate(page, per_page=10, error_out=True)
    else:
        table = Book.query.filter_by(provenance=text).order_by(Book.id)
        count = table.count()
        print('debug数量', count)
        table_paginate = table.paginate(page, per_page=10, error_out=True)
    flash(f"查询成功,查询到{count}条结果！", category='info')
    return table_paginate
