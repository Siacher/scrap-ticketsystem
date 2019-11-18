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
    db.connection.commit()

    return jsonify({"message": "ok"})


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
