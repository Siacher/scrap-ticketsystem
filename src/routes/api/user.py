from flask import Blueprint, request, jsonify, g
import bcrypt

from . import db
from src.shared.authentification import Auth

user_route = Blueprint('user', __name__)


def generate_hash(password):
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(14))


def check_hash(password, _hash):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(_hash, 'utf-8'))


@user_route.route('/user', methods=['GET'])
def get_all():
    result = db.get_all("user")
    return jsonify({"data": result})


@user_route.route('/user/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("user", _id))


@user_route.route('/user', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO user(email, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['email'], generate_hash(data['password']), data['first_name'], data['last_name']))

        sql = "SELECT * FROM user WHERE email=%s"
        cursor.execute(sql, (data['email'],))

        result = cursor.fetchone()

        print(data['password'])
        print(result['password'])
        print(check_hash(data['password'], result['password']))

        if not check_hash(data['password'], result['password']):
            return jsonify({'message': 'mail or password invalid'})
        else:
            token = Auth.generate_token(result['id'])

    db.connection.commit()

    return jsonify({'token': token})


@user_route.route('/user/<_id>', methods=['DELETE'])
def delete(_id):

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM user WHERE id =%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})


@user_route.route('/user/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = 'UPDATE user SET email=%s, password=%s, first_name=%s, last_name=%s  WHERE id=%s'
        cursor.execute(sql, (data['email'], generate_hash(data['password']), data['first_name'], data['last_name'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("user", _id))


@user_route.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM user WHERE email=%s"
        cursor.execute(sql, (data['email'], ))

        result = cursor.fetchone()

        print(data['password'])
        print(result['password'])
        print(check_hash(data['password'], result['password']))

        if not check_hash(data['password'], result['password']):
            return jsonify({'message': 'mail or password invalid'})
        else:
            token = Auth.generate_token(result['id'])

    db.connection.commit()

    return jsonify({'token': token})


@user_route.route('/user/by_token', methods=['GET'])
@Auth.auth_required
def get_user_by_token():
    _id =g.user['id']
    return jsonify(db.get_one_by_id("user", _id))


@user_route.route('/user/me/can_change/<t_id>', methods=['GET'])
@Auth.auth_required
def can_change(t_id):
    _id =g.user['id']

    with db.connection.cursor() as cursor:
        sql = 'SELECT ug.name FROM user as u JOIN user_in_group as uig on u.id = uig.user_id JOIN user_group as ug on uig.group_id = ug.id WHERE u.id=%s'
        cursor.execute(sql, (_id, ))
        result = cursor.fetchall()

        ticket = db.get_one_by_id('ticket', t_id)

        value = False
        for item in result:
            if item['name'] == "admin":
                value = True

            if item['name'] == "processor" and ticket['assign_to'] == _id:
                value = True

        return jsonify({"message": str(value).lower()})


@user_route.route('/user/me/is_admin', methods=['GET'])
@Auth.auth_required
def is_admin():
    _id =g.user['id']

    with db.connection.cursor() as cursor:
        sql = 'SELECT ug.name FROM user as u JOIN user_in_group as uig on u.id = uig.user_id JOIN user_group as ug on uig.group_id = ug.id WHERE u.id=%s'
        cursor.execute(sql, (_id, ))
        result = cursor.fetchall()

        value = False
        for item in result:
            if item['name'] == "admin":
                value = True

        return jsonify({"message": str(value).lower()})


@user_route.route('/user/add_group', methods=['POST'])
@Auth.auth_required
def add_group():
    _id = g.user['id']

    # user_id and group_id
    data = request.get_json()

    with db.connection.cursor() as cursor:

        sql = 'SELECT ug.name FROM user as u JOIN user_in_group as uig on u.id = uig.user_id JOIN user_group as ug on uig.group_id = ug.id WHERE u.id=%s'
        cursor.execute(sql, (_id,))
        result = cursor.fetchall()

        value = False
        for item in result:
            if item['name'] == "admin":
                value = True

        message = "not authorized"
        if value:
            sql = "INSERT INTO user_in_group(user_id, group_id) VALUES (%s, %s)"
            cursor.execute(sql, (data['user_id'], data['group_id']))
            message = "ok"

    db.connection.commit()

    return jsonify({'message': message})


@user_route.route('/user/change_group', methods=['POST'])
@Auth.auth_required
def change_group():
    _id = g.user['id']

    # user_id and group_id, and new_group_id
    data = request.get_json()

    with db.connection.cursor() as cursor:

        sql = 'SELECT ug.name FROM user as u JOIN user_in_group as uig on u.id = uig.user_id JOIN user_group as ug on uig.group_id = ug.id WHERE u.id=%s'
        cursor.execute(sql, (_id,))
        result = cursor.fetchall()

        value = False
        for item in result:
            if item['name'] == "admin":
                value = True

        message = "not authorized"
        if value:
            sql = "UPDATE user_in_group SET user_id = %s, group_id = %s WHERE user_id = %s AND group_id = %s"
            cursor.execute(sql, (data['user_id'], data['new_group_id'], data['user_id'], data['group_id'],))
            message = "ok"

    db.connection.commit()

    return jsonify({'message': message})


@user_route.route('/user/group', methods=['GET'])
@Auth.auth_required
def group():
    _id = g.user['id']

    # user_id and group_id
    data = request.get_json()

    with db.connection.cursor() as cursor:

        sql = 'SELECT ug.name FROM user as u JOIN user_in_group as uig on u.id = uig.user_id JOIN user_group as ug on uig.group_id = ug.id WHERE u.id=%s'
        cursor.execute(sql, (_id,))
        result = cursor.fetchall()

        value = False
        for item in result:
            if item['name'] == "admin":
                value = True

        message = "not authorized"
        if value:
            sql = "SELECT u.id as user_id, u.first_name, u.last_name, u.email, ug.name, ug.id as group_id FROM user as u JOIN user_in_group as uig on u.id = uig.user_id JOIN user_group as ug on uig.group_id = ug.id"
            cursor.execute(sql)
            message = cursor.fetchall()

    db.connection.commit()

    return jsonify({'message': message})