from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('记住密码')
    submit = SubmitField('登录')


class RetrievePasswordForm(FlaskForm):
    email = StringField('请输入账号绑定的邮箱:', validators=[DataRequired()])
    # verification_code = StringField('验证码',validators=[DataRequired()])
    # send_code = SubmitField('发送验证码')
    submit = SubmitField('确定')
