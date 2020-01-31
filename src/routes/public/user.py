import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from src.forms import ManageUserForm, LoginForm, RegisterForm
from src.routes.api import db
from src.routes.public import LUser
from src.shared.choiceSort import choice_sort

index_route = Blueprint('user', __name__)


def generate_hash(password):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(14))


def check_hash(password, _hash):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(_hash, 'utf-8'))

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
        redirect(url_for('user.manage_user'))

    return render_template('manage_user.html', forms=user_forms, subsite=True)

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
                    return redirect(url_for('user.login'))

                if check_hash(form.passwort.data, user['password']):
                    user_login = LUser(user['id'], user['email'], user['first_name'], user['last_name'],
                                       user['password'])
                    login_user(user_login, remember=form.remember_me.data)
                    return redirect(url_for('index.index'))

                flash('Invalid username or password')
                print("wrong password")
                return redirect(url_for('user.login'))

    return render_template('login.html', form=form, login=True)


@index_route.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('user.login'))


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
            return redirect(url_for('user.login'))

    return render_template('register.html', form=form)