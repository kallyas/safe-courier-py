from .resources import Parcels

def parcel_routes(api):
    api.add_resource(Parcels, '/parcels/create', '/parcels/<int:parcel_id>', '/parcels')