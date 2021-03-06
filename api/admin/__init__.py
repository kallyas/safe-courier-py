from .resources import AdminResource, GeneralInfo

def admin_routes(api):
    api.add_resource(AdminResource, 
    '/api/v1/admin/parcels/<int:parcel_id>',
    '/api/v1/admin/parcels'
    )
    api.add_resource(GeneralInfo, '/')