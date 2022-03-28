from .resources import UsersResource

def users_route(api):
    api.add_resource(UsersResource, '/api/v1/users', '/api/v1/user/<int:user_id>', endpoint='users')