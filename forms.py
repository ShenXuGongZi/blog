from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = TextAreaField('内容', validators=[DataRequired()])
    image = FileField('上传图片', validators=[FileAllowed(['jpg', 'png', 'gif'], '只允许上传图片!')])
    submit = SubmitField('提交')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('new_password', message='两次输入的密码必须相同')])
    submit = SubmitField('修改密码')
