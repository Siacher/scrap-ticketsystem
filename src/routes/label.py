from flask import Blueprint

from . import db
from src.database.label import Label

label_route = Blueprint('label', __name__)


@label_route.route('/')
def get_label():
    print(Label.get_all(db))
    return "hello world"