from flask import Blueprint, request, jsonify

from . import db

user_group_route = Blueprint('user_group', __name__)


@user_group_route.route('/user_group', methods=['GET'])
def get_all():
    result = db.get_all("user_group")
    return jsonify({"data": result})


@user_group_route.route('/user_group/<_id>', methods=['GET'])
def get_one(_id):
    return jsonify(db.get_one_by_id("user_group", _id))

