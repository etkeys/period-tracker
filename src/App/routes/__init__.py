import os
import secrets
from PIL import Image
from flask import flash, render_template, redirect, url_for, request, abort
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user

from App import app, db, crypto, mail
from App.forms import (LoginForm, RegistrationForm, UpdateAccountForm,
                       RequestResetForm, ResetPasswordForm)
from App.models import User
from .route_safety import url_has_allowed_host_and_scheme

# As routes get more complex, may need to separate them out into
# their own files.

def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    new_f_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_images', new_f_name)
    # form_picture.save(picture_path)

    # scale down large images
    output_size = (240, 240)
    i = Image.open(form_picture)
    i.thumbnail = output_size

    i.save(picture_path)
    return new_f_name


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.display_name = form.display_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')

        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.display_name.data = current_user.display_name
        form.email.data = current_user.email

    image_file = url_for('static', filename=f"profile_images/{current_user.image_file}")
    return render_template(
        'account.html',
        title='Account',
        user_image_file=image_file,
        form=form)

@app.route('/attribution')
def attribution():
    return render_template('attribution.html', title='Attributions')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypto.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            if next_page is None:
                return redirect(url_for('home'))

            # TODO Need to protect against open redirect vulnerability
            if not url_has_allowed_host_and_scheme(next_page, request.host):
                return abort(400)

            return redirect(next_page)
        else:
            flash(f'Email or Password incorrect!', 'error')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = crypto.generate_password_hash(form.password.data).decode('utf-8')
        display_name = form.email.data.split('@')[0]

        user = User(email=form.email.data, display_name=display_name, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # TODO need to test this
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    # TODO Need to change sender
    msg = Message(
        'Password reset request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )

    # using _external=True will cause the url to be an absolute url instead of relative
    msg.body = f'''
To reset your password, visit the following link:

{url_for(reset_with_token, token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
'''

    mail.send(msg)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    # TODO need to test this
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('The token provided is invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = crypto.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()

        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_with_token.html', title='Reset Password', form=form)