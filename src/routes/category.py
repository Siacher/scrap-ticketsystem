from flask import Blueprint, request, jsonify

from . import db

category_route = Blueprint('category', __name__)


@category_route.route('/category', methods=['GET'])
def get_all():
    result = db.get_all("category")
    return jsonify({"data": result})


@category_route.route('/category/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("category", _id))


@category_route.route('/category', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO category(text) VALUES (%s)"
        cursor.execute(sql, (data['text']))
    db.connection.commit()

    return jsonify({"message": "ok"})


@category_route.route('/category/<_id>', methods=['DELETE'])
def delete(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM category WHERE id =%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})


@category_route.route('/category/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "UPDATE category SET text=%s WHERE id=%s"
        cursor.execute(sql, (data['text'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("category", _id))