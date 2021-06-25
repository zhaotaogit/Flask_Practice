from flask import render_template, flash, redirect, url_for, session,request

from app import app, db
from app.forms import RegisterForm, LoginForm, RetrievePasswordForm
from app.models import User
# from app.func import add_user, search_user, is_pwd_true, search_email
from flask_login import login_user, login_required, logout_user, current_user

app.config['SECRET_KEY'] = "long SECRET_KEY"


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


@app.route('/Retrieve_password/', methods=['GET', 'POST'])
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


@app.route('/admin/select_book/')
def select_book():
    return render_template('select_book.html')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))
