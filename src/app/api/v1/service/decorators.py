import os
from functools import wraps

from flask import request
from flask_restx import reqparse

from src.app.api.v1.service.datastore.token_datastore import TokenDataStore

SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            body = request.args
            access_data = TokenDataStore.get_user_data_from_token(token=body['access_token'], secret_key=SECRET_KEY)
            if access_data["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return {"message": "Admins only!"}, 403

        return decorator

    return wrapper
