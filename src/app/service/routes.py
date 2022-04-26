from src.app.service.auth import LoginApi, RefreshAPI, RegistrationAPI, LogoutAPI, HistoryAuthAPI, ChangeAuthDataAPI
from src.app.service.roles_api import RolesAPI, UserRolesAPI


def initialize_routes(api):
    api.add_resource(RegistrationAPI, '/api/v1/registration')
    api.add_resource(LoginApi, '/api/v1/login')
    api.add_resource(LogoutAPI, '/api/v1/logout')
    api.add_resource(RefreshAPI, '/api/v1/refresh')
    api.add_resource(HistoryAuthAPI, '/api/v1/auth_history')
    api.add_resource(ChangeAuthDataAPI, '/api/v1/auth_change')
    api.add_resource(RolesAPI, '/api/v1/roles')
    api.add_resource(UserRolesAPI, '/api/v1/user-roles')
