from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email()
        ])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired()
        ])

    remember = BooleanField('Remember me')

    submit = SubmitField('Login')
