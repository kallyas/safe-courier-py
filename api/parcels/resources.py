from datetime import timedelta


from models import Parcel
from flask_restful import Resource, reqparse
from flask_jwt_extended import ( jwt_required, get_jwt_claims )


class Parcels(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='This field is required', required=True)
        self.parser.add_argument('weight', type=float, help='This field is required', required=True)
        self.parser.add_argument('price', type=float, help='This field is required', required=True)
        self.parser.add_argument('destination', type=str, help='This field is required', required=True)
        self.parser.add_argument('current_location', type=str, help='This field is required', required=True)
        self.parser.add_argument('status', type=str, help='This field is required', required=True)

    

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        parcel = Parcel(
            name=data['name'],
            weight=data['weight'],
            price=data['price'],
            destination=data['destination'],
            current_location=data['current_location'],
            status=data['status'],
            user_id=get_jwt_claims()['id']
        )
        parcel.save_to_db()
        return parcel.json(), 201

    @jwt_required
    def get(self):
        return {'parcels': [parcel.json() for parcel in Parcel.query.all()]}

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
    def delete(self):
        data = self.parser.parse_args()
        parcel = Parcel.query.filter_by(id=data['id']).first()

        if not parcel:
            return {'message': 'Parcel not found'}, 404
        parcel.delete_from_db()
        return {'message': 'Parcel deleted'}