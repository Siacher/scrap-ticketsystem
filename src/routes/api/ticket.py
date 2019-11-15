from flask import Blueprint, request, jsonify

from . import db

ticket_route = Blueprint('ticket', __name__)


@ticket_route.route('/ticket', methods=['GET'])
def get_all():
    result = db.get_all("ticket")
    return jsonify({"data": result})


@ticket_route.route('/ticket/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("ticket", _id))


@ticket_route.route('/ticket/me', methods=['GET'])
@Auth.auth_required
def get_my_tickets(_id):
    uid = g.user['id']
    with db.connection.cursor() as cursor:
        sql = "SELECT * FROM ticket WHERE 'created_by' = %S"
        cursor.execute(sql, (uid))
        # TODO: return values
    db.connection.commit()


    return jsonify(db.get_one_by_id("ticket", _id))


@ticket_route.route('/ticket', methods=['POST'])
def insert():
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "INSERT INTO ticket(header, text,  category_id, status_id, comment_id, child_ticket, prio_id, assign_to, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (data['header'], data['text'],  data['category_id'], data['status_id'], data['comment_id'], data['child_ticket'], data['prio_id'], data['assign_to'], data['created_by']))
    db.connection.commit()

    return jsonify({"message": "ok"})


@ticket_route.route('/ticket/<_id>', methods=['DELETE'])
def delete(_id):

    with db.connection.cursor() as cursor:
        sql = "DELETE FROM ticket WHERE id =%s"
        cursor.execute(sql, (_id, ))
    db.connection.commit()

    return jsonify({"message": "ok"})


@ticket_route.route('/ticket/<_id>', methods=['PUT'])
def update(_id):
    data = request.get_json()

    with db.connection.cursor() as cursor:
        sql = "UPDATE ticket SET header=%s, text=%s, category_id=%s, status_id=%s, comment_id=%s, child_ticket=%s, prio_id=%s, assign_to=%s, created_by=%s WHERE id=%s"
        cursor.execute(sql, (data['header'], data['text'],  data['category_id'], data['status_id'], data['comment_id'], data['child_ticket'], data['prio_id'], data['assign_to'], data['created_by'], _id))
    db.connection.commit()

    return jsonify(db.get_one_by_id("ticket", _id))