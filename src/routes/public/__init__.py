from flask_login import LoginManager, UserMixin
from src.routes.api import db
login = LoginManager()


class LUser(UserMixin):
    def __init__(self, _id, email, first_name, last_name, password):
        self.id = _id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


@login.user_loader
def load_user(_id):
    user = db.get_one_by_id('user', _id)
    return LUser(user['id'], user['email'], user['first_name'], user['last_name'], user['password'])
