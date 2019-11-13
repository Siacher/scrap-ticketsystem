from flask import Blueprint, request, jsonify

from . import db

status_route = Blueprint('status', __name__)


@status_route.route('/status', methods=['GET'])
def get_all():
    result = db.get_all("status")
    return jsonify({"data": result})


@status_route.route('/status/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("status", _id))


@status_route.route('/status', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO status(text, completion, color) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['text'], data['completion'], data['color']))
    db.connection.commit()

    return jsonify({"message": "ok"})


@status_route.route('/status/<_id>', methods=['DELETE'])
def delete(_id):

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM status WHERE id =%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})


@status_route.route('/status/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "UPDATE status SET text=%s, completion=%s, color=%s WHERE id=%s"
        cursor.execute(sql, (data['text'], data['completion'], data['color'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("status", _id))