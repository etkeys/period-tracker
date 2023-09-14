from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import InputRequired, Email, ValidationError

from App.models import User

class RequestResetForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email()
        ])

    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        # get the user that already exists in the database
        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError('There is no account with that email. You must register first.')