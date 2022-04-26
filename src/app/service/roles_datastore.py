import uuid
from typing import Optional

from src.app.db.db import db, session_scope
from src.app.db.db_models import Permission, Role, RolePermission, UserRole


class RolesCRUD:
    @staticmethod
    def get_all_roles():
        """
        Получить все роли

        :return: roles: Все роли
        """
        roles = Role.query.all()
        return roles

    @staticmethod
    def create_role(role: str, description: Optional[str]):
        """
        Создать роль

        :param role: Название новой роли
        :param description: Описание новой роли

        :return: new_role: Созданая роль
        """
        new_role = Role(id=uuid.uuid4(), role_type=role, description=description)
        with session_scope():
            db.session.add(new_role)
        return new_role

    @staticmethod
    def update_role(role_id: uuid.uuid4(), role: str, description: Optional[str]):
        """
        Изменить роль

        :param role_id: id изменяемой роли
        :param role: Новое название роли
        :param description: Новое описание роли

        :return: None
        """
        if not description:
            with session_scope():
                Role.query.filter_by(id=role_id).update(
                    {'role_type': role})
        else:
            with session_scope():
                Role.query.filter_by(id=role_id).update(
                    {'role_type': role, 'description': description})

    @staticmethod
    def delete_role(role_id: uuid.uuid4()):
        """
        Удалить роль

        :param role_id: id удаляемой роли

        :return: None
        """
        with session_scope():
            Role.query.filter_by(id=role_id).delete()

    @staticmethod
    def check_user_role(user_id: uuid.uuid4()):
        """
        Проверить роли и права пользователя

        :param user_id: id пользователя

        :return: user_roles: Роли пользователя и права ролей
        """
        with session_scope():
            records = db.session.query(UserRole, Role, RolePermission, Permission) \
                .filter(UserRole.user_id == user_id,
                        UserRole.role_id == Role.id,
                        Role.id == RolePermission.role_id,
                        Permission.id == RolePermission.permission_id).all()
        user_roles = []
        for user_role, role, role_permission, permission in records:
            user_roles.append([role, permission])
        return user_roles

    @staticmethod
    def add_role_to_user(user_id: uuid.uuid4(), role_id: uuid.uuid4()):
        """
        Добавить пользователю роль

        :param user_id: id пользователя
        :param role_id: id роли

        :return: None
        """
        user_role = UserRole(id=uuid.uuid4(), user_id=user_id, role_id=role_id)
        with session_scope():
            db.session.add(user_role)

    @staticmethod
    def delete_user_role(user_id: uuid.uuid4(), role_id: uuid.uuid4()):
        """
        Удалить роль у пользователя

        :param user_id: id пользователя
        :param role_id: id роли

        :return: None
        """
        with session_scope():
            UserRole.query.filter_by(user_id=user_id, role_id=role_id).delete()
