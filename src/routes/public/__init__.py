from flask_login import LoginManager, UserMixin
login = LoginManager()


class LUser(UserMixin):
    def __init__(self, _id, email, first_name, last_name, password):
        self.id = _id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
