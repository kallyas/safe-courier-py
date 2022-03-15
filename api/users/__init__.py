from .resources import Users

def users_route(api):
    api.add_resource(Users, '/users', '/user/<int:id>', endpoint='users')