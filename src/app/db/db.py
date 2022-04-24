import os
from contextlib import contextmanager

from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv("../app/config/.env")

db = SQLAlchemy()
migrate = Migrate()


def init_db(app: Flask):
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{os.getenv("POSTGRES_USER")}:' \
        f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/{os.getenv("POSTGRES_DB")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    migrate.init_app(app, db)


@contextmanager
def session_scope():
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
