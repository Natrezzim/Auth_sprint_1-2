import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api

from src.app.api.v1.service.role_service.roles_api import roles
from src.app.db.db import init_db
from src.app.db.db_models import db
from src.app.api.v1.service.auth_service.auth_api import auth
from src.app.api.v1.routes.routes import initialize_routes

load_dotenv(f'{os.getcwd()}/.env')

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(roles)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

api = Api(app, version='1.0', title='Auth API',
    description='Сервис авторизации')

ns = api.namespace('auth', description='authentication')

migrate = Migrate(app, db)

init_db(app)

initialize_routes(api)

if __name__ == '__main__':
    app.run()
