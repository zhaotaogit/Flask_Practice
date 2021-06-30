from flask import render_template, flash, redirect, url_for, session, request

from app import app, db
from app.forms import RegisterForm, LoginForm, RetrievePasswordForm, SelectBookForm, AddBookForm, DelBookForm, \
    RetrievePasswordSubForm, ResetPasswordForm
from app.models import User, Book, Recording
from app.func import send_mail
from flask_login import login_user, login_required, logout_user, current_user

dit = {}


# 首页视图
@app.route('/')
@login_required
def home():
    # print(current_user.username)
    return render_template('index.html', name=current_user.username, title='首页')


# 书籍销售记录视图
@app.route('/recording/<int:page>')
@login_required
def recording(page):
    if not page or page < 1:
        page = 1
    table_paginate = Recording.query.order_by(Recording.timer.desc()).paginate(page, per_page=10, error_out=True)
    return render_template('recording.html', table_page=table_paginate)


# 个人中心视图
@app.route('/personal_center')
@login_required
def personal_center():
    return render_template('personal_center.html')


# 浏览书籍信息视图
@app.route('/bookinfo/<int:page>')
@login_required
def bookinfo(page):
    if not page or page < 1:
        page = 1
    table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10, error_out=True)
    return render_template('bookinfo.html', table_page=table_paginate)


# 购买书籍视图
@app.route('/buybook/', methods=['GET', 'POST'])
@login_required
def buybook():
    if request.method == 'GET':
        book_id = request.args.get('book_id')
        if not book_id:
            return render_template('buybook.html')
        book = Book.query.filter_by(id=book_id).first()
        return render_template('buybook.html', book=book)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        num = form_data.get('num')
        print(form_data)
        print(num)
        book_id = form_data.get('book_id')
        if not book_id:
            flash("你还没有选择要购买的书!", category='info')
            print('你还没有选择要购买的书！')
            return redirect(url_for('buybook'))
        else:
            book = Book.query.filter_by(id=book_id).first()
            book_num = book.count
            if book_num >= int(num):
                book.count -= int(num)
                db.session.commit()
                flash(f"购买成功,共花费:{int(num)*book.price}元!", category='info')
                print('购买成功！')
                recording = Recording(name=book.name, category=book.category, author=book.author, img=book.img,
                                      provenance=book.provenance, price=book.price, num=int(num), info="售出")
                db.session.add(recording)
                db.session.commit()
                return redirect(url_for('buybook', book_id=book_id))
            else:
                flash("库存不足,请联系管理员!", category='info')
                print('库存不足,请联系管理员!')
                return redirect(url_for('buybook', book_id=book_id))
    return redirect(url_for('buybook'))


# 用户登录视图
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
                flash('用户名或密码错误!', category='info')
        else:
            flash("登录的用户不存在!", category='info')
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
    form_sub = RetrievePasswordSubForm()
    if form.validate_on_submit():
        print('123')
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        print(email)
        if user:
            flag, code = send_mail(email)
            print(flag)
            if flag:
                flash('验证码发送成功，请前往邮箱查看!', category='info')
                form.email.data = email
                dit[email] = code
                return redirect(url_for('retrievepasswordsub', email=email))
            else:
                flash("验证码发送失败!", category='info')
                return redirect(url_for('retrieve_password'))
        else:
            flash("输入的邮箱不存在!", category='info')
            return redirect(url_for('retrieve_password'))
    if form_sub.validate_on_submit():
        return redirect(url_for('retrieve_password'))
    return render_template('retrieve_password.html', form=form, form_sub=form_sub)


@app.route('/send_email/<string:email>')
def send_email(email):
    flag, code = send_mail(email)
    print(flag)
    if flag:
        flash('验证码发送成功，请前往邮箱查看!', category='info')
        dit[email] = code
        return redirect(url_for('retrievepasswordsub', email=email))
    else:
        flash("验证码发送失败!", category='info')
        return redirect(url_for('retrieve_password'))

@app.route('/retrievepasswordsub/<string:email>', methods=['GET', 'POST'])
def retrievepasswordsub(email):
    form = RetrievePasswordForm()
    form.email.data = email
    if form.validate_on_submit():
        print(dit)
        code = dit[email]
        print(code)
        vcode = form.verification_code.data
        print(vcode)
        user = User.query.filter_by(email=email).first()
        # print(code, vcode)
        # print(type(code),type(vcode))
        # print(code == vcode)
        if str(code) == vcode:
            return redirect(url_for('reset_password', username=user.username))
        else:
            flash("验证码错误！", category='info')
            return redirect(url_for('retrievepasswordsub', email=email))
    return render_template('retrievepasswordsub.html', form=form,email=email)


@app.route('/reset_password/<string:username>',methods=['GET','POST'])
def reset_password(username):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        newpassword = form.password.data
        user = User.query.filter_by(username=username).first()
        user.password = newpassword
        db.session.commit()
        flash('密码修改成功!', category='info')
        return redirect(url_for('reset_password',username=username))
    return render_template('reset_password.html',form=form)

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
    # 修改书籍信息
    if alter_form.validate_on_submit():
        print('debug:测试点击2')
        print(alter_form.bool.data)
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
        else:
            flash("要修改的书籍不存在！", category="info")
        return render_template('select_book.html', alter_form=alter_form, table_page=table_paginate)
    return render_template('select_book.html', form=form, table_page=table_paginate)


@app.route('/del_book/<int:page>')
def del_book(page):
    remove_form = DelBookForm()
    if not page or page < 1:
        page = 1
    # if
    table_paginate = Book.query.order_by(Book.id).paginate(page, per_page=10, error_out=True)
    return render_template('del_book.html', table_page=table_paginate, remove_form=remove_form, page=page)


@app.route('/del_book/del_id/<int:id>')
def delete_book(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('del_book', page=0))


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
