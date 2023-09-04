from flask_login import UserMixin
from App import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    display_name = db.Column(db.String(254), nullable=False, default='')
    image_file = db.Column(db.String(100), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    cycles = db.relationship('Cycle', backref='person', lazy=True)

    def __repr__(self):
        return f"User('{self.display_name}', '{self.email}', '{self.image_file}')"