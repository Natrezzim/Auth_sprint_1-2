import os
import uuid

from flask import Blueprint, jsonify, request
from flask_restx import Resource, reqparse

from flask_restx import Namespace
from src.app.api.v1.service.decorators import admin_required
from src.app.api.v1.service.datastore.roles_datastore import RolesCRUD
from src.app.utils.pagination import get_paginated_list

roles = Blueprint('roles', __name__)

ROLE_START_PAGE = os.getenv('ROLE_START_PAGE')
ROLE_PAGE_LIMIT = os.getenv('ROLE_PAGE_LIMIT')

role_namespace = Namespace("roles", description='roles')


@role_namespace.doc(params={'id': 'ID Роли', 'role': 'Тип роли', 'description': 'Описание', 'access_token': 'access_token'})
class RolesAPI(Resource):
    """
    Логика работы метода api/v1/roles
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=uuid.uuid4(), required=False, help="id")
    parser.add_argument('role', type=str, required=False, help="role")
    parser.add_argument('description', type=str, required=False, help="description")
    parser.add_argument('access_token', type=str, required=True, help="access_token")

    @staticmethod
    @admin_required()
    def get():
        return jsonify(get_paginated_list(RolesCRUD.get_all_roles(), '/api/v1/roles',
                                          start=request.args.get('start', ROLE_START_PAGE),
                                          limit=request.args.get('limit', ROLE_PAGE_LIMIT)))

    @staticmethod
    @admin_required()
    def post():
        body = request.args
        try:
            return jsonify({'message': 'Role Created'},
                           RolesCRUD.create_role(body["role"], body["description"]))
        except Exception as e:
            return str(e)

    @staticmethod
    @admin_required()
    def put():
        body = request.args
        try:
            RolesCRUD.update_role(body["id"], body["role"], body["description"])
            return {'message': 'Role Updated'}
        except Exception as e:
            return str(e)

    @staticmethod
    @admin_required()
    def delete():
        body = request.args
        try:
            RolesCRUD.delete_role(body.get("id"))
            return {'message': 'Role Deleted'}
        except Exception as e:
            return str(e)


@role_namespace.doc(params={'user_id': 'ID Пользователя', 'role_id': 'ID Роли'})
class UserRolesAPI(Resource):
    """
        Логика работы метода api/v1/user-roles
        """

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=uuid.uuid4(), required=False, help="user_id")
    parser.add_argument('role_id', type=uuid.uuid4(), required=False, help="role_id")

    @staticmethod
    @admin_required()
    def get():
        body = request.args
        return jsonify(RolesCRUD.check_user_role(body["user_id"]))

    @staticmethod
    @admin_required()
    def post():
        body = request.args
        try:
            jsonify(RolesCRUD.add_role_to_user(body["user_id"], body["role_id"]))
            return {'message': 'Role added to User'}
        except Exception as e:
            return str(e)

    @staticmethod
    @admin_required()
    def delete():
        body = request.args
        try:
            jsonify(RolesCRUD.delete_user_role(body["user_id"], body["role_id"]))
            return {'message': 'User role deleted'}
        except Exception as e:
            return str(e)
