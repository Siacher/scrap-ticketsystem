from functools import wraps
import jwt
import datetime
from flask import json, Response, request, g, redirect
from src.routes.api import db


class Auth:

    @staticmethod
    def generate_token(uid):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': uid
            }
            return jwt.encode(
                payload,
                'I bin d Bene',
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            return f'error in generating user token {e}'

    @staticmethod
    def decode_token(token):
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, 'I bin d Bene')
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again with a new token'}
            return re

    @staticmethod
    def auth_required(func):

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'token' not in request.headers:
                return redirect('/login')

            token = request.headers.get('token')
            data = Auth.decode_token(token)
            if data['error']:
                return redirect('/login')

            user_id = data['data']['user_id']
            check_user = db.get_one_by_id(table="user", _id=user_id)

            if not check_user:
                return redirect('/login')

            g.user = {'id': user_id}
            return func(*args, **kwargs)
        return decorated_auth
