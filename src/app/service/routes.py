from .auth import RegistrationAPI, LoginApi, RefreshAPI, RolesAPI


def initialize_routes(api):
    api.add_resource(RegistrationAPI, '/api/v1/registration')
    api.add_resource(LoginApi, '/api/v1/login')
    api.add_resource(RefreshAPI, '/api/v1/refresh')
    api.add_resource(RolesAPI, '/api/v1/roles')
