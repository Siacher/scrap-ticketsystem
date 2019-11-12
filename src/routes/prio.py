from flask import Blueprint, request, jsonify

from . import db

prio_route = Blueprint('prio', __name__)


@prio_route.route('/prio', methods=['GET'])
def get_all():
    result = db.get_all("prio")
    return jsonify({"data": result})


@prio_route.route('/prio/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("prio", _id))


@prio_route.route('/prio', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO prio(prio, text, color, icon) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['prio'], data['text'], data['color'], data['icon']))
    db.connection.commit()

    return jsonify({"message": "ok"})


@prio_route.route('/prio/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "UPDATE prio SET prio=%s, text=%s, color=%s, icon=%s WHERE id=%s"
        cursor.execute(sql, (data['prio'], data['text'], data['color'], data['icon'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("prio", _id))


@prio_route.route('/prio/<_id>', methods=['DELETE'])
def delete(_id):

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM prio WHERE id=%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})