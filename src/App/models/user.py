import datetime
from flask_login import UserMixin
import jwt
from App import app, db, login_manager

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

    def get_reset_token(self, expires_sec=1800):
        # this was from the flask tutorial, but itsdangerious doesn't have
        # the TimedJSONWebSerializer anymore
        # s = TimedSerializer(app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': self.id}).decode('utf-8')

        # now we use pyjwt (ref: https://stackoverflow.com/a/72091078)
        token = jwt.encode(
            {
                'user_id': self.id,
                'expires':
                    datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(seconds=expires_sec)
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return token

    @staticmethod
    def verify_reset_token(token):
        # this was from the flask tutorial, but itsdangerios doesn't have
        # the TimedJSONWebSerializer anymore
        # s = TimedSerializer(app.config['SECRET_KEY'])
        # try:
        #     user_id = data.loads(token)['user_id']
        # except:
        #     return None

        # now we use pyjwt (ref: https://stackoverflow.com/a/72091078)
        try:
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=60),
                algorithms=["HS256"]
            )
            user_id = data.get('user_id')
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.display_name}', '{self.email}', '{self.image_file}')"