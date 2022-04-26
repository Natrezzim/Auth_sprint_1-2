from src.app.service.auth import RegistrationAPI, LoginApi, RefreshAPI
from src.app.service.roles_api import RolesAPI, UserRolesAPI


def initialize_routes(api):
    api.add_resource(RegistrationAPI, '/api/v1/registration')
    api.add_resource(LoginApi, '/api/v1/login')
    api.add_resource(RefreshAPI, '/api/v1/refresh')
    api.add_resource(RolesAPI, '/api/v1/roles')
    api.add_resource(UserRolesAPI, '/api/v1/user-roles')
