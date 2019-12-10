from flask import Blueprint, render_template

from src.shared.authentification import Auth

index_route = Blueprint('index', __name__)


@index_route.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@index_route.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@index_route.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@index_route.route('/ticket/<_id>', methods=['GET'])
def ticket(_id):
    return render_template('ticket.html')


@index_route.route('/create_ticket', methods=['GET'])
def create_ticket():
    return render_template('create_ticket.html')


@index_route.route('/create_category', methods=['GET'])
def create_category():
    return render_template('create_category.html')


@index_route.route('/create_priority', methods=['GET'])
def create_priority():
    return render_template('create_priority.html')


@index_route.route('/manage_user', methods=['GET'])
def log_req():
    return render_template('manage_user.html')
