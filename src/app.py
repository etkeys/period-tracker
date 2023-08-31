from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'develop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default_profile.jpg')
    password = db.Column(db.String(60), nullable=False)
    cycles = db.relationship('Cycle', backref='person', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.image_file}')"


class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Cycle('{self.user_id}', '{self.start_date}', '{self.end_date}')"

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

if __name__ == '__main__':
    app.run()