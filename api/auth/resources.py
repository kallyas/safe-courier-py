from datetime import timedelta

from models import User, RevokedToken
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt, create_refresh_token,
    get_jwt_claims, jwt_refresh_token_required,
)
from flask_restful import Resource, reqparse


class RegisterUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('first_name', type=str, required=True)
        self.parser.add_argument('last_name', type=str, required=True)
        self.parser.add_argument('address', type=str, required=True)
        self.parser.add_argument('phone', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def post(self):
        data = self.parser.parse_args()

        current_user = User.find_by_email(data['email'])

        if current_user and current_user['email'] == data['email'] and current_user['username'] == data['username']:
            return {'message': 'User already exists'}, 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            phone_number=data['phone'],
            password=User.generate_hash(data['password']),
            role_id=2
        )

        new_user.save_to_db()

        return {'message': 'User created successfully'}, 201

    @jwt_required
    def put(self):
        self.parser.add_argument(
            'id', type=int, help='user id is required', required=True)
        data = self.parser.parse_args()

        user = User.find_by_id(data['id'])

        if not user:
            return {'message': 'User with id {} not fount'.format(data['id'])}, 404

        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.address = data['address']
        user.phone = data['phone']
        user.updated_by = get_jwt_claims()['id']
        user.update()

        return {'message': 'User {} updated successfully'.format(data['first_name'])}, 200


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', help='This field cannot be blank', required=True, type=str)
        parser.add_argument(
            'password', help='This field cannot be blank', required=True, type=str)

        data = parser.parse_args()

        current_user = User.find_by_email(data['email'])

        if not current_user:
            return {'message': 'User by {} not found'.format(data['email'])}, 404

        if User.verify_hash(data['password'], current_user.password):
            expires = timedelta(days=1)
            identity = {
                'id': current_user.id,
                'role': current_user.role_id
            }
            access_token = create_access_token(
                identity=identity, expires_delta=expires)
            refresh_token = create_refresh_token(identity=identity)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': current_user.id,
                    'email': current_user.email,
                    'role': current_user.role_id,
                }
            }, 200
        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        expires = timedelta(days=1)
        access_token = create_access_token(
            identity=current_user, expires_delta=expires)
        return {'access_token': access_token}, 200


class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        print(jti)
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save_to_db()
            return {'message': 'Successfully logged out'}, 200
        except:
            return {'message': 'Something went wrong'}, 500


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Successfully logged out'}, 200
        except:
            return {'message': 'Something went wrong'}, 500
