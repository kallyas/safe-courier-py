from models import Parcel
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, get_jwt_claims
)
from api.utils.schemas import ParcelSchema

parcel_schema = ParcelSchema()
parcels_schema = ParcelSchema(many=True)


class AdminResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required
    def put(self, parcel_id):
        self.parser.add_argument(
            'status', type=str, required=True, help='Status cannot be left blank')
        self.parser.add_argument('current_location', type=str,
                                 required=True, help='Current location cannot be left blank')

        if not get_jwt_claims()['role'] == 1:
            return {'message': 'Admin access only'}, 403
        data = self.parser.parse_args()
        parcel = Parcel.query.filter_by(id=parcel_id).first()
        if parcel:
            parcel.status = data['status']
            parcel.current_location = data['current_location']
            parcel.update()
            return parcel_schema.dump(parcel), 200
        return {'message': 'Parcel not found'}, 404

    @jwt_required
    def delete(self, parcel_id):
        if not get_jwt_claims()['role'] == 1:
            return {'message': 'Admin access only'}, 403
        data = self.parser.parse_args()
        parcel = Parcel.query.filter_by(id=parcel_id).first()
        if parcel:
            Parcel.delete_from_db(id=parcel_id)
            return {'message': 'Parcel deleted'}, 200
        return {'message': 'Parcel not found'}, 404
