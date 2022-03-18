from models import User
from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required
)
from api.utils.schemas import UserSchema

user_schema = UserSchema()
user_schema_many = UserSchema(many=True)


class Users(Resource):

    @jwt_required
    def get(self, id=None):
        if id:
            user = User.query.filter_by(id=id).first()
            if not user:
                return {"message": "User not found"}, 404
            return user_schema.dump(user), 200
        users = User.query.all()
        return user_schema_many.dump(users)

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        data = parser.parse_args()

        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'User not found'}, 404

        user = User(**data)
        user.update()

        return {'message': 'User {} updated successfully'.format(data['username'])}

    @jwt_required
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'message': 'User not found'}, 404

        user.delete_from_db()

        return {'message': 'User {} deleted successfully'.format(id)}
