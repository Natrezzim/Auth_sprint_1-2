import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

from src.app.db.db import init_db
from src.app.db.db_models import db
from src.app.service.auth import auth
from src.app.service.routes import initialize_routes

load_dotenv(f'{os.getcwd()}/.env')

app = Flask(__name__)

app.register_blueprint(auth)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

api = Api(app)

migrate = Migrate(app, db)

init_db(app)

initialize_routes(api)

if __name__ == '__main__':
    app.run()
