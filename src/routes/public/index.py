from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from src.routes.api import db
from . import LUser
from src.shared.authentification import Auth
import bcrypt

from src.forms import LoginForm, CreateTicketForm

index_route = Blueprint('index', __name__)


def check_hash(password, _hash):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(_hash, 'utf-8'))


@index_route.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('index.login'))
    else:
        with db.connection.cursor() as cursor:
            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.created_by = %s"
            cursor.execute(sql, (current_user.id,))
            my_tickets = cursor.fetchall()

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.assign_to = %s"
            cursor.execute(sql, (current_user.id,))
            ass_tickets = cursor.fetchall()

    return render_template('index.html', my_tickets=my_tickets, ass_tickets=ass_tickets)


@index_route.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            with db.connection.cursor() as cursor:
                sql = "SELECT * FROM user WHERE email=%s"
                cursor.execute(sql, (form.email.data,))
                user = cursor.fetchone()

                if user is None:
                    flash('Invalid username or password')
                    print("no user")
                    return redirect(url_for('index.login'))

                if check_hash(form.passwort.data, user['password']):
                    flash('Invalid username or password')
                    print("wrong password")
                    return redirect(url_for('index.login'))

                user_login = LUser(user['id'], user['email'], user['first_name'], user['last_name'], user['password'])

                login_user(user_login, remember=form.remember_me.data)
                return redirect(url_for('index.index'))

    return render_template('login.html', form=form)


@index_route.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index.login'))


@index_route.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@index_route.route('/ticket/<_id>', methods=['GET'])
def ticket(_id):
    with db.connection.cursor() as cursor:
        sql = "SELECT t.header as header, t.text as text, p.text as prio, c.text as category FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.id = %s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()

    return render_template('ticket.html', ticket=result)


@index_route.route('/create_ticket', methods=['GET'])
def create_ticket():
    form = CreateTicketForm()
    return render_template('create_ticket.html', form=form)


@index_route.route('/create_category', methods=['GET'])
def create_category():
    return render_template('create_category.html')


@index_route.route('/create_priority', methods=['GET'])
def create_priority():
    return render_template('create_priority.html')


@index_route.route('/manage_user', methods=['GET'])
def log_req():
    return render_template('manage_user.html')
