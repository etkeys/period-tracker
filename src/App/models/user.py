from App import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default_profile.jpg')
    password = db.Column(db.String(60), nullable=False)
    cycles = db.relationship('Cycle', backref='person', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.image_file}')"