from .resources import Users

def users_route(api):
    api.add_resource(Users, '/api/v1/users', '/api/v1/user/<int:id>', endpoint='users')