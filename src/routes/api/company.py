from flask import Blueprint, request, jsonify

from . import db

company_route = Blueprint('company', __name__)


@company_route.route('/company', methods=['GET'])
def get_all():
    result = db.get_all("company")
    return jsonify({"data": result})


@company_route.route('/company/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("company", _id))


@company_route.route('/company', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO company(name) VALUES (%s)"
        cursor.execute(sql, (data['name'], ))
    db.connection.commit()

    return jsonify({"message": "ok"})


@company_route.route('/company/<_id>', methods=['DELETE'])
def delete(_id):

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM company WHERE id =%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})


@company_route.route('/company/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "UPDATE status SET name=%s WHERE id=%s"
        cursor.execute(sql, (data['name'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("company", _id))