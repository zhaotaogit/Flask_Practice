# # -*- coding = utf-8 -*-
# # @Time : 2021/6/24 16:13
# # @File : test.py
# # @Software: PyCharm
# import sqlite3
#
# username = '1787417712'
#
# conn = sqlite3.connect('data.db')
# # conn.row_factory = sqlite3.Row
# curs = conn.cursor()
# sql = f"select username,password from User where username = '{username}'"
# # print(sql)
# result = curs.execute(sql).fetchone()
# curs.close()
# conn.close()
# print(result[1])
# # for i in result:
# #     print(i)
#
#
from flask import Flask,render_template,request
from werkzeug import secure_filename
from flask_wtf.file import FileField
from flask_wtf import FlaskForm
import os

class PhotoForm(FlaskForm):
    photo = FileField('Your photo')


app = Flask(__name__)

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        # 将用户提交的数据组合到一起，都放到表单中验证
        form = PhotoForm()
        if form.validate():
            desc = form.desc.data
            avatar = form.avatar.data
            filename = secure_filename(avatar.filename)  # 文件名安全
            avatar.save(os.path.join('./', filename))
            return '文件上传成功'
        else:
            print(form.errors)
            return "fail"



if __name__ == '__main__':
    app.run()