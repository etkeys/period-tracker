from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, ValidationError

from App.models import User

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired()
        ])
    confirm_password = PasswordField(
        'Confirm password',
        validators=[
            InputRequired(),
            EqualTo('password')
        ])

    submit = SubmitField('Reset password')
