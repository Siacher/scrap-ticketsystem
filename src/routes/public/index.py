from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from src.routes.api import db
from . import LUser
from src.shared.authentification import Auth
import bcrypt

from src.forms import LoginForm, RegisterForm, CreateTicketForm

index_route = Blueprint('index', __name__)


def generate_hash(password):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(14))


def check_hash(password, _hash):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(_hash, 'utf-8'))


@index_route.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('index.login'))
    else:
        with db.connection.cursor() as cursor:
            sql = "SELECT ug.name, ug.id FROM user_group as ug JOIN user_in_group uig on ug.id = uig.group_id JOIN user u on uig.user_id = u.id WHERE u.id = %s"
            cursor.execute(sql, (current_user.id,))
            group = cursor.fetchone()

            user_group = 'default'
            try:
                if group['name']:
                    user_group = group['name']
            except TypeError as NOUSERGROUP:
                print(NOUSERGROUP)

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.created_by = %s"
            cursor.execute(sql, (current_user.id,))
            my_tickets = cursor.fetchall()

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.assign_to = %s"
            cursor.execute(sql, (current_user.id,))
            ass_tickets = cursor.fetchall()

    return render_template('index.html', my_tickets=my_tickets, ass_tickets=ass_tickets, user_group=user_group)


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
                    user_login = LUser(user['id'], user['email'], user['first_name'], user['last_name'], user['password'])
                    login_user(user_login, remember=form.remember_me.data)
                    return redirect(url_for('index.index'))

                flash('Invalid username or password')
                print("wrong password")
                return redirect(url_for('index.login'))

    return render_template('login.html', form=form)


@index_route.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index.login'))


@index_route.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            sql = "INSERT INTO user(email, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (form.email.data, generate_hash(form.passwort.data), form.first_name.data, form.last_name.data))

            sql = "SELECT * FROM user WHERE email=%s"
            cursor.execute(sql, (form.email.data,))

            result = cursor.fetchone()

            sql = "INSERT INTO user_in_group(user_id, group_id) VALUES (%s, %s)"
            cursor.execute(sql, (result['id'], 2))

            db.connection.commit()
            return redirect(url_for('index.login'))

    return render_template('register.html', form=form)


@index_route.route('/ticket/<_id>', methods=['GET'])
def ticket(_id):
    with db.connection.cursor() as cursor:
        sql = "SELECT t.header as header, t.text as text, p.text as prio, c.text as category FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.id = %s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()

    return render_template('ticket.html', ticket=result)


@index_route.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    prio_return = db.get_all("prio")
    prio = [(i['id'], i['text']) for i in prio_return]

    category_return = db.get_all("category")
    category = [(i['id'], i['text']) for i in category_return]

    form = CreateTicketForm()
    form.prio.choices = prio
    form.category.choices = category

    if form.submit():
        header = form.header.data
        text = form.text.data
        prio_id = form.prio.data
        category_id = form.category.data
        user_id = current_user.id

        with db.connection.cursor() as cursor:
            sql = "INSERT INTO ticket(header, text,  category_id, prio_id, created_by) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (header, text, category_id, prio_id, user_id))
        db.connection.commit()
        return redirect(url_for('index.index'))

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
