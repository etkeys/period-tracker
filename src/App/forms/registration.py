from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email, ValidationError

from App.models import User

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

    def validate_email(self, email):
        # get the user that already exists in the database
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('This email is already registered.')


