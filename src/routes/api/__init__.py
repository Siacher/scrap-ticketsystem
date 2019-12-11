from src.database import Database
from src.routes.public import login

db = Database()


@login.user_loader
def load_user(_id):
    return db.get_one_by_id('user', _id)
