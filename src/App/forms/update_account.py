from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import InputRequired, Email, ValidationError, Length

from App.models import User

class UpdateAccountForm(FlaskForm):
    display_name = StringField(
        'Display name',
        validators=[
            InputRequired(),
            Length(min=1)
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email()
        ])
    picture = FileField(
        'Update profile picutre',
        validators=[FileAllowed(['jpg', 'png'])]
    )

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            # get the user that already exists in the database
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('This email is already registered.')


