from flask import Blueprint, request, jsonify

from . import db

comment_route = Blueprint('comment', __name__)


@comment_route.route('/comment', methods=['GET'])
def get_all():
    result = db.get_all("comment")
    return jsonify({"data": result})


@comment_route.route('/comment/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("comment", _id))


@comment_route.route('/comment', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO comment(header, text, created_by, created_at, ticket_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['header'], data['text'], data['created_by'], data['created_at'], data['ticket_id']))
    db.connection.commit()

    return jsonify({"message": "ok"})


@comment_route.route('/comment/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "UPDATE comment SET header=%s, text=%s, created_by=%s, created_at=%s, ticket_id=%s WHERE id=%s"
        cursor.execute(sql, (data['header'], data['text'], data['created_by'], data['created_at'], data['ticket_id'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("comment", _id))


@comment_route.route('/comment/<_id>', methods=['DELETE'])
def delete(_id):

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM comment WHERE id=%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})