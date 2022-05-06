
import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from src.app.miscellaneous.jaeger import init_jaeger
from src.app.miscellaneous.jaeger_config import configure_tracer
from src.app.miscellaneous.rate_limit import init_rate_limit
from src.app.api.v1.routes.routes import initialize_routes
from src.app.api.v1.service.auth_service.auth_api import auth, auth_namespace
from src.app.api.v1.service.role_service.cli_commands import adm_cmd
from src.app.api.v1.service.role_service.roles_api import role_namespace, roles
from src.app.db.db import init_db
from src.app.oauth.oauth import init_oauth

load_dotenv(f'{os.getcwd()}/.env')

app = Flask(__name__)

jwt = JWTManager(app)

api = Api(app, version='1.0', title='Auth API',
          description='Сервис авторизации', doc='/doc/')

app.config["SECRET_KEY"] = '3212gregbergqfwwe'

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

init_db(app)
init_oauth(app)
initialize_routes(api)
app.register_blueprint(auth)
app.register_blueprint(roles)
app.register_blueprint(adm_cmd)
api.add_namespace(role_namespace)
api.add_namespace(auth_namespace)
init_rate_limit(app)
init_jaeger(app)
configure_tracer()
FlaskInstrumentor().instrument_app(app)

if __name__ == '__main__':
    app.run()
