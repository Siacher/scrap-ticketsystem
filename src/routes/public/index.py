from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from src.routes.api import db
from . import LUser
from pymysql.err import IntegrityError
from src.shared.authentification import Auth
import bcrypt
import datetime
import scss

from src.forms import LoginForm, RegisterForm, CreateTicketForm, ManageUserForm, ManageCategroyForm, ManagePrioForm, \
    ManageStatusForm, CreateCommentForm, UpdateTicketForm

from src.shared.choiceSort import choice_sort

from jinja2 import Environment as Jinja2Environment
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension
from scss import Compiler

assets_env = AssetsEnvironment('./static', '/')
jinja2_env = Jinja2Environment(extensions=[AssetsExtension])
jinja2_env.assets_environment = assets_env

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

            sql = "SELECT * FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id WHERE t.assign_to = NULL AND t.created_by != %s"
            cursor.execute(sql, (current_user.id,))
            not_ass_tickets = cursor.fetchall()

    return render_template('index.html', my_tickets=my_tickets, ass_tickets=ass_tickets,
                           not_ass_tickets=not_ass_tickets, user_group=user_group)


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
                    user_login = LUser(user['id'], user['email'], user['first_name'], user['last_name'],
                                       user['password'])
                    login_user(user_login, remember=form.remember_me.data)
                    return redirect(url_for('index.index'))

                flash('Invalid username or password')
                print("wrong password")
                return redirect(url_for('index.login'))

    return render_template('login.html', form=form, login=True)


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
            cursor.execute(sql, (
                form.email.data, generate_hash(form.passwort.data), form.first_name.data, form.last_name.data))

            sql = "SELECT * FROM user WHERE email=%s"
            cursor.execute(sql, (form.email.data,))

            result = cursor.fetchone()

            sql = "INSERT INTO user_in_group(user_id, group_id) VALUES (%s, %s)"
            cursor.execute(sql, (result['id'], 2))

            company_sql = "INSERT INTO company(name) VALUES (%s)"
            cursor.execute(company_sql, (
                form.company.data
            ))

            db.connection.commit()
            return redirect(url_for('index.login'))

    return render_template('register.html', form=form)


@index_route.route('/ticket/<_id>', methods=['GET', 'POST'])
def ticket(_id):
    with db.connection.cursor() as cursor:
        sql = "SELECT t.header as header, t.text as text, p.text as prio, p.color as prio_color, c.text as category, s.text as status, s.color as status_color FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id LEFT JOIN status as s on t.status_id = s.id WHERE t.id = %s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()

    form = CreateCommentForm()
    if form.is_submitted() and form.submit.data:
        header = form.header.data
        text = form.text.data
        created_at = datetime.datetime.now()
        created_by = current_user.id
        ticket_id = _id

        with db.connection.cursor() as cursor:
            sql = "INSERT INTO comment(header, text, created_at, created_by, ticket_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (header, text, created_at, created_by, ticket_id))
        db.connection.commit()
        comments = db.get_all_join_ticket_id(ticket_id)
        return redirect(url_for('index.ticket', _id=_id))

    comments = db.get_all_join_ticket_id(_id)
    return render_template('ticket.html', ticket=result, form=form, comments=comments, subsite=True, _ticket=_id)


@index_route.route('/ticket/<_id>/update', methods=['GET', 'POST'])
def update_ticket(_id):
    with db.connection.cursor() as cursor:
        sql = "SELECT t.header as header, t.text as text, p.text as prio, p.color as prio_color, c.text as category, s.text as status, s.color as status_color FROM ticket as t LEFT JOIN prio as p on t.prio_id = p.id LEFT JOIN category as c on t.category_id = c.id LEFT JOIN status as s on t.status_id = s.id WHERE t.id = %s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()

    prio_return = db.get_all("prio")
    prio = [i['text'] for i in prio_return]
    _prio = choice_sort(prio, result['prio'])

    category_return = db.get_all("category")
    category = [i['text'] for i in category_return]
    _category = choice_sort(category, result['category'])

    user_return = db.get_all("user")
    user = [(i['id'], f"{i['first_name']} {i['last_name']} | {i['email']}") for i in user_return]

    status_return = db.get_all("status")
    status = [i['text'] for i in status_return]
    _status = choice_sort(status, result['status'])

    form = UpdateTicketForm()
    form.prio.choices = _prio
    form.category.choices = _category
    form.status.choices = _status
    form.user.choices = user

    form.header.data = result["header"]
    form.text.data = result["text"]

    if form.is_submitted():
        header = form.header.data
        text = form.text.data
        user_id = form.user.data
        with db.connection.cursor() as cursor:
            sql = "SELECT id FROM prio WHERE text = %s"
            cursor.execute(sql, (form.prio.choices[int(form.prio.data)][1],))
            prio_id = cursor.fetchone()['id']

            sql = "SELECT id FROM status WHERE text = %s"
            cursor.execute(sql, (form.status.choices[int(form.status.data)][1],))
            status_id = cursor.fetchone()['id']

            sql = "SELECT id FROM category WHERE text = %s"
            cursor.execute(sql, (form.category.choices[int(form.category.data)][1],))
            category_id = cursor.fetchone()['id']
            try:
                sql = "UPDATE ticket set header = %s, text = %s,  category_id = %s, prio_id= %s, status_id= %s, assign_to= %s  WHERE ticket.id = %s "
                cursor.execute(sql, (header, text, category_id, prio_id, status_id, user_id, _id))
            except IntegrityError as ConstraintError:
                flash("Kann nicht gelöscht werden. Wird noch verwendet")
            finally:
                return redirect(url_for('index.index'))
    db.connection.commit()

    return render_template('update_ticket.html', form=form, subsite=True)


@index_route.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    prio_return = db.get_all("prio")
    prio = [(i['id'], i['text']) for i in prio_return]

    category_return = db.get_all("category")
    category = [(i['id'], i['text']) for i in category_return]

    status_return = db.get_all("status")
    status = [(i['id'], i['text']) for i in status_return]

    form = CreateTicketForm()
    form.prio.choices = prio
    form.category.choices = category
    form.status.choices = status

    if form.is_submitted():
        header = form.header.data
        text = form.text.data
        prio_id = form.prio.data
        category_id = form.category.data
        status_id = form.status.data
        user_id = current_user.id

        with db.connection.cursor() as cursor:
            sql = "INSERT INTO ticket(header, text,  category_id, prio_id, status_id, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (header, text, category_id, prio_id, status_id, user_id))
        db.connection.commit()
        return redirect(url_for('index.index'))

    return render_template('create_ticket.html', form=form, subsite=True)


@index_route.route('/manage_category', methods=['GET', 'POST'])
def manage_category():
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM category"
        cursor.execute(sql)

        categories = cursor.fetchall()

        form = ManageCategroyForm()
        if form.submit.data and form.is_submitted():
            sql = "INSERT INTO category(text) VALUES (%s)"
            cursor.execute(sql, (form.text.data,))
            return redirect(url_for('index.manage_category'))

        if request.method == 'POST' and request.form['delete']:
            cat_id = request.form['delete']
            sql = "DELETE FROM category WHERE id = %s"
            cursor.execute(sql, (cat_id,))
            return redirect(url_for('index.manage_category'))

        db.connection.commit()

    return render_template('manage_category.html', form=form, categories=categories, subsite=True)


@index_route.route('/manage_prio', methods=['GET', 'POST'])
def manage_prio():
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM prio"
        cursor.execute(sql)

        prio = cursor.fetchall()

        form = ManagePrioForm()
        if form.submit.data and form.is_submitted():
            print(form.color.data)
            sql = "INSERT INTO prio(text, prio, color) VALUES (%s, %s, %s)"
            cursor.execute(sql, (form.text.data, form.prio.data, str(form.color.data)))
            return redirect(url_for('index.manage_prio'))

        if request.method == 'POST' and request.form['delete']:
            prio_id = request.form['delete']
            sql = "DELETE FROM prio WHERE id = %s"
            cursor.execute(sql, (prio_id,))
            return redirect(url_for('index.manage_prio'))

        db.connection.commit()

    return render_template('manage_prio.html', form=form, prio=prio, subsite=True)


@index_route.route('/manage_status', methods=['GET', 'POST'])
def manage_status():
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM status"
        cursor.execute(sql)

        status = cursor.fetchall()

        form = ManageStatusForm()

        if request.method == 'POST' and request.form['delete']:
            status_id = request.form['delete']
            sql = "DELETE FROM status WHERE id = %s"
            cursor.execute(sql, (status_id,))
            return redirect(url_for('index.manage_status'))

        if form.submit.data and form.is_submitted():
            sql = "INSERT INTO status(text, completion, color) VALUES (%s, %s, %s)"
            cursor.execute(sql, (form.text.data, form.completion.data, str(form.color.data)))
            return redirect(url_for('index.manage_status'))

        db.connection.commit()

    return render_template('manage_status.html', form=form, status=status, subsite=True)


@index_route.route('/manage_user', methods=['GET', 'POST'])
def manage_user():
    user_forms = []

    update = False

    with db.connection.cursor() as cursor:
        sql = 'SELECT u.id, u.first_name , u.last_name, u.email, ug.id as group_id, ug.name FROM user as u JOIN user_in_group as uig on u.id = uig.user_id LEFT JOIN user_group as ug on uig.group_id = ug.id'
        cursor.execute(sql)
        users = cursor.fetchall()

        for user in users:
            user_group_return = db.get_all("user_group")
            user_group = [i['name'] for i in user_group_return]

            form = ManageUserForm(prefix=user['email'])
            form.first_name.label = user['first_name']
            form.last_name.label = user['last_name']
            form.email.label = user['email']
            _user_group = choice_sort(user_group, user['name'])
            form.user_group.choices = _user_group
            user_forms.append(form)

            if form.submit.data and form.is_submitted():
                sql = "SELECT id FROM user WHERE email = %s"
                cursor.execute(sql, (user['email'],))
                user_id = cursor.fetchone()['id']

                sql = "SELECT id FROM user_group WHERE name = %s"
                cursor.execute(sql, (form.user_group.choices[int(form.user_group.data)][1],))
                group_id = cursor.fetchone()

                sql = "UPDATE user_in_group SET group_id = %s WHERE user_id = %s AND group_id = %s"
                cursor.execute(sql, (group_id['id'], user_id, user['group_id']))
                update = True
    db.connection.commit()

    if update:
        redirect(url_for('index.manage_user'))

    return render_template('manage_user.html', forms=user_forms, subsite=True)


@index_route.route('/kanban', methods=['GET', 'POST'])
def kanban():
    with db.connection.cursor() as cursor:
        sql = "SELECT id, text, color FROM status ORDER BY completion"
        cursor.execute(sql)
        status = cursor.fetchall()

        for stat in status:
            sql = "SELECT header, ticket.id, c.email, a.email FROM ticket LEFT JOIN user as c ON ticket.created_by = c.id LEFT JOIN user as a ON ticket.assign_to = a.id WHERE status_id = %s"
            cursor.execute(sql, (stat['id'],))
            stat['tickets'] = cursor.fetchall()

    return render_template('kanban.html', subsite=True, status=status)
