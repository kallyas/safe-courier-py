from .resources import AdminResource

def admin_routes(api):
    api.add_resource(AdminResource, '/api/v1/admin/parcels/<int:parcel_id>')