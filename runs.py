# -*- coding = utf-8 -*-
# @Time : 2021/6/24 15:07
# @File : runs.py
# @Software: PyCharm

from app import app

if __name__ == '__main__':
    app.run(debug=True, port=5001,host='0.0.0.0')
