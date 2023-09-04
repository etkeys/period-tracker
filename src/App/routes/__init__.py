from flask import flash, render_template, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from App import app, db, crypto
from App.forms import LoginForm, RegistrationForm
from App.models import User
from .route_safety import url_has_allowed_host_and_scheme

# As routes get more complex, may need to separate them out into
# their own files.

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

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
        user = User(email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
