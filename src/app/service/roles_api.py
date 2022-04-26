import uuid

from flask import Blueprint, jsonify
from flask_restful import Resource, reqparse, request

from src.app.service.roles_datastore import RolesCRUD

auth = Blueprint('role', __name__)


class RolesAPI(Resource):
    """
    Логика работы метода api/auth/roles
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=uuid.uuid4(), required=False, help="id")
    parser.add_argument('role', type=str, required=False, help="role")
    parser.add_argument('description', type=str, required=False, help="description")

    @staticmethod
    def get():
        return jsonify(RolesCRUD.get_all_roles())

    @staticmethod
    def post():
        body = request.get_json()
        try:
            return jsonify({'message': 'Role Created'},
                           RolesCRUD.create_role(body.get("role"), body.get("description")))
        except Exception as e:
            return str(e)

    @staticmethod
    def put():
        body = request.get_json()
        try:
            RolesCRUD.update_role(body.get("id"), body.get("role"), body.get("description"))
            return {'message': 'Role Updated'}
        except Exception as e:
            return str(e)

    @staticmethod
    def delete():
        body = request.get_json()
        try:
            RolesCRUD.delete_role(body.get("id"))
            return {'message': 'Role Deleted'}
        except Exception as e:
            return str(e)


class UserRolesAPI(Resource):
    """
        Логика работы метода api/auth/user-roles
        """

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=uuid.uuid4(), required=False, help="user_id")
    parser.add_argument('role_id', type=uuid.uuid4(), required=False, help="role_id")

    @staticmethod
    def get():
        body = request.get_json()
        return jsonify(RolesCRUD.check_user_role(body.get("user_id")))

    @staticmethod
    def post():
        body = request.get_json()
        try:
            jsonify(RolesCRUD.add_role_to_user(body.get("user_id"), body.get("role_id")))
            return {'message': 'Role added to User'}
        except Exception as e:
            return str(e)

    @staticmethod
    def delete():
        body = request.get_json()
        try:
            jsonify(RolesCRUD.delete_user_role(body.get("user_id"), body.get("role_id")))
            return {'message': 'User role deleted'}
        except Exception as e:
            return str(e)
