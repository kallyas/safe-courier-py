from .resources import UserLogin, LogoutAccess, TokenRefresh, LogoutRefresh, RegisterUser

def auth_routes(api):
    api.add_resource(UserLogin, '/api/v1/auth/login')
    api.add_resource(RegisterUser, '/api/v1/auth/register')
    api.add_resource(LogoutAccess, '/api/v1/auth/logout')
    api.add_resource(TokenRefresh, '/api/v1/auth/refresh')
    api.add_resource(LogoutRefresh, '/api/v1/auth/logout/refresh')