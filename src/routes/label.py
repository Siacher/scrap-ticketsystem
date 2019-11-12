from flask import Blueprint, request, jsonify

from . import db

label_route = Blueprint('label', __name__)


@label_route.route('/label', methods=['GET'])
def get_all():
    result = db.get_all("label")
    return jsonify({"data": result})


@label_route.route('/label/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("label", _id))


@label_route.route('/label', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO label(text, color) VALUES (%s, %s)"
        cursor.execute(sql, (data['text'], data['color']))
    db.connection.commit()

    return jsonify({"message": "ok"})