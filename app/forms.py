from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextField
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


class SelectBookForm(FlaskForm):
    operatin_select = SelectField(
        label='选择操作的',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '查询'), (2, '修改'), (3, '删除')],
        default=1,
        coerce=int
    )
    select = SelectField(
        label='选择查询的类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '书籍编号'), (2, '书名'), (3, '类别'), (4, '作者'), (5, '出版社')],
        default=1,
        coerce=int
    )

    text = TextField('要查寻的内容', validators=[DataRequired()])

    submit = SubmitField('确定')


# 书号，书名，类别，作者，出版社，价格，库存量
class AddBookForm(FlaskForm):
    id = StringField("书籍编号", validators=[DataRequired()])
    name = StringField("书名", validators=[DataRequired()])
    category = StringField("类别", validators=[DataRequired()])
    author = StringField("作者", validators=[DataRequired()])
    # 出版社
    provenance = StringField("出版社", validators=[DataRequired()])
    price = StringField("价格", validators=[DataRequired()])
    num = StringField("数量", validators=[DataRequired()])
    bool = BooleanField("已确认")
    submit = SubmitField('确定')


class DelBookForm(FlaskForm):
    id = StringField("书籍编号", validators=[DataRequired()])
    bool = BooleanField("已确认")
    submit = SubmitField('确定')


