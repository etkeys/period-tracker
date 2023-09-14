from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# TODO need to get mail username and password
app.config['MAIL_USERNAME'] = 'get_from_environment?'
app.config['MAIL_PASSWORD'] = 'get_from_environment?'
app.config['SECRET_KEY'] = 'develop'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
crypto = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from App.routes import *
