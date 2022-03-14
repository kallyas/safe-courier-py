from .resources import UserLogin, LogoutAccess, TokenRefresh, LogoutRefresh, RegisterUser

def auth_routes(api):
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(RegisterUser, '/auth/register')
    api.add_resource(LogoutAccess, '/auth/logout')
    api.add_resource(TokenRefresh, '/auth/refresh')
    api.add_resource(LogoutRefresh, '/auth/logout/refresh')