from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user_name = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SetpointForm(FlaskForm):
    set_point = HiddenField('set_point')
    temperature = HiddenField('temperature')
    time = HiddenField('time')
    battery = HiddenField('battery')


class AwayForm(FlaskForm):
    away = HiddenField('away')

