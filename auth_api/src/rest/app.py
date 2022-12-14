import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_qrcode import QRcode
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from src.rest.miscellaneous.xcaptcha_config import init_captcha
from src.rest.miscellaneous.jaeger import init_jaeger
from src.rest.miscellaneous.jaeger_config import configure_tracer
from src.rest.miscellaneous.rate_limit import init_rate_limit
from src.rest.api.v1.routes.routes import initialize_routes
from src.rest.api.v1.service.auth_service.auth_api import auth, auth_namespace
from src.rest.api.v1.service.role_service.cli_commands import adm_cmd
from src.rest.api.v1.service.role_service.roles_api import role_namespace, roles
from src.data.db.db import init_db
from src.rest.oauth.oauth import init_oauth

load_dotenv(f'{os.getcwd()}/.env')

app = Flask(__name__)

jwt = JWTManager(app)

api = Api(app, version='1.0', title='Auth API',
          description='Сервис авторизации', doc='/doc/')

app.config["SECRET_KEY"] = '3212gregbergqfwwe'

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
QRcode(app)
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
init_captcha(app)

if __name__ == '__main__':
    app.run()
