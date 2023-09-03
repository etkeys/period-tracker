from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email

class RegistrationForm(FlaskForm):
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
    confirm_password = PasswordField(
        'Confirm password',
        validators=[
            InputRequired(),
            EqualTo('password')
        ])

    submit = SubmitField('Sign Up')