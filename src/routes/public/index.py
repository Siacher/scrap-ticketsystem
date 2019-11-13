from flask import Blueprint, render_template

from src.shared.authentification import Auth

index_route = Blueprint('index', __name__)


@index_route.route('/', methods=['GET'])
@Auth.auth_required
def index():
    return render_template('index.html')


@index_route.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@index_route.route('/login_req', methods=['GET'])
@Auth.auth_required
def log_req():
    return render_template('index.html')
