from flask import flash, render_template, redirect, url_for

from App import app
from App.forms import LoginForm, RegistrationForm

# As routes get more complex, may need to separate them out into
# their own files.

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.email.data == 'admin@pt.com' and form.password.data == 'password'):
            flash(f'Welcome, {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Email or Password incorrect!', 'error')
    return render_template('login.html', title='Login', form=form)