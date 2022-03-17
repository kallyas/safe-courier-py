from .resources import Parcels

def parcel_routes(api):
    api.add_resource(Parcels,
     '/api/v1/parcels/create', 
     '/api/v1/parcels/<int:parcel_id>', 
     '/api/v1/parcels',
     '/api/v1/users/<int:user_id>/parcels'
     )