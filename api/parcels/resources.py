from datetime import timedelta

from flask import jsonify
from models import Parcel
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_claims)
from api.utils.schemas import ParcelSchema

parcel_schema = ParcelSchema()
parcels_schema = ParcelSchema(many=True)


class Parcels(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'name', type=str, help='This field is required', required=True)
        self.parser.add_argument('weight', type=float,
                                 help='This field is required', required=True)
        self.parser.add_argument(
            'price', type=float, help='This field is required', required=True)
        self.parser.add_argument(
            'destination', type=str, help='This field is required', required=True)
        self.parser.add_argument(
            'current_location', type=str, help='This field is required', required=True)
        self.parser.add_argument(
            'status', type=str, help='This field is required', required=True)
        self.parser.add_argument(
            'description', type=str, help='This field is required', required=True)
        self.parser.add_argument(
            'location', type=str, help='This field is required', required=True)

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        parcel = Parcel(
            name=data['name'],
            weight=data['weight'],
            price=data['price'],
            description=data['description'],
            location=data['location'],
            destination=data['destination'],
            current_location=data['current_location'],
            status=data['status'],
            user_id=get_jwt_claims()['id']
        )
        parcel.save_to_db()
        return {'message': 'Parcel created successfully'}, 201

    @jwt_required
    def get(self, parcel_id=None, user_id=None):
        if parcel_id:
            parcel = Parcel.query.filter_by(id=parcel_id).first()
            if parcel:
                return parcel_schema.dump(parcel)
            return {'message': 'Parcel not found'}, 404
        elif user_id:
            parcels = Parcel.query.filter_by(user_id=user_id).all()
            if parcels:
                return parcels_schema.dump(parcels)
            return {'message': 'Parcels by user not found'}, 404
        else:
            parcels = Parcel.query.all()
            return {
                'count': Parcel.count_all(),
                'parcels': parcels_schema.dump(parcels)
            }

    @jwt_required
    # user can only update their own parcels for the following fields:
    # name, weight, destination,
    def put(self):
        data = self.parser.parse_args()
        parcel = Parcel.query.filter_by(id=data['id']).first()

        if not parcel:
            return {'message': 'Parcel not found'}, 404

        parcel.name = data['name']
        parcel.weight = data['weight']
        parcel.destination = data['destination']
        parcel.save_to_db()
        return parcel.json()

    @jwt_required
    def delete(self, parcel_id):
        parcel = Parcel.query.filter_by(id=parcel_id).first()
        if not parcel:
            return {'message': 'Parcel not found'}, 404
        parcel.delete_from_db(parcel_id)
        return {'message': 'Parcel deleted'}
